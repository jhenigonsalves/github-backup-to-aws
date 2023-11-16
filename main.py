from typing import Dict, List
import requests
from ratelimit import limits, sleep_and_retry
import json
from datetime import date
import boto3
from botocore.exceptions import ClientError

# Api Call Restrictions
period_in_seconds = 60
calls_per_period = 30


def turn_bool_string_to_bool(str_: str) -> bool:
    """_summary_

    Args:
        str_ (str): string that looks like a bool, e.g. 'false'

    Returns:
        bool
    """
    return eval(str_.title())


def filter_repository_by_owner(
    repositories: List[Dict],
    backup_only_owner_repos: str,
    token: str = None,
) -> List[Dict]:
    """
    Receive repositories and filter them by owner_name. Return the subset of repositories filtered.
    If apply_filter = False, return repositories as is.
    """
    backup_only_owner_repos = turn_bool_string_to_bool(backup_only_owner_repos)
    if backup_only_owner_repos:
        owner_name = get_owner_name(token)
        repos_filter_by_owner = [
            repo for repo in repositories if repo["owner"] == owner_name
        ]
        return repos_filter_by_owner
    return repositories


def get_metadata(
    token: str,
    backup_only_owner_repos: str,
    bucket_prefix: str,
    bucket_name: str,
    boto3_session: boto3.Session,
) -> List[Dict]:
    metadata = []
    max_per_page = 100  # Max value accepted by github api

    my_headers = {"Authorization": f"Bearer {token}"}

    page = 1
    params = {"per_page": max_per_page, "page": page}
    response = get_url(
        "https://api.github.com/user/repos", headers=my_headers, params=params
    )
    response_json = response.json()

    while len(response_json):
        aux_metadata = [
            {
                "name": repo["name"],
                "owner": repo["full_name"].split("/")[0],
                "is_private": repo["private"],
            }
            for repo in response_json
        ]
        metadata = metadata + aux_metadata

        page = page + 1
        params = {"per_page": max_per_page, "page": page}
        response = get_url(
            "https://api.github.com/user/repos", headers=my_headers, params=params
        )
        response_json = response.json()

    metadata = filter_repository_by_owner(metadata, backup_only_owner_repos, token)
    metadata_json = json.dumps(metadata)
    write_metadata_backup_file_to_s3(
        metadata_json,
        bucket_prefix,
        bucket_name,
        boto3_session,
    )
    return metadata


def write_metadata_backup_file_to_s3(
    metadata_json: json,
    bucket_prefix: str,
    bucket_name: str,
    boto3_session: boto3.Session,
):
    prefix = get_prefix(bucket_prefix)
    object_name = f"{prefix}/metadata.json"
    s3 = boto3_session.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=object_name, Body=metadata_json)


def get_current_date_formatted() -> str:
    today = date.today()
    today_formatted = today.strftime("%Y-%m-%d")
    today_str = str(today_formatted)
    return today_str


def get_prefix(bucket_prefix: str) -> str:
    date_prefix = get_current_date_formatted()
    prefix_str = f"{bucket_prefix}/{date_prefix}"
    return prefix_str


def write_repository_zip_backup_to_s3(
    repos: bytes,
    owner: str,
    repo_name: str,
    ext: str,
    bucket_prefix: str,
    bucket_name: str,
    boto3_session: boto3.Session,
):
    prefix = get_prefix(bucket_prefix)
    object_name = f"{prefix}/{owner}_{repo_name}.{ext}"

    s3 = boto3_session.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=object_name, Body=repos)


@sleep_and_retry
@limits(calls=calls_per_period, period=period_in_seconds)
def get_url(url: str, headers: Dict = {}, params: Dict = {}):
    if params:
        return requests.get(url, headers=headers, params=params)
    return requests.get(url, headers=headers)


def download_repos(
    token: str,
    backup_only_owner_repos: str,
    bucket_prefix: str,
    bucket_name: str,
    boto3_session: boto3.Session,
    ext: str = "zip",
    ref: str = "",
) -> None:
    metadata = get_metadata(
        token,
        backup_only_owner_repos,
        bucket_prefix,
        bucket_name,
        boto3_session,
    )
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    full_names = [(repo["owner"], repo["name"]) for repo in metadata]

    for owner, repo_name in full_names:
        url = f"https://api.github.com/repos/{owner}/{repo_name}/{ext}ball/{ref}"
        response = get_url(url, headers=headers)
        try:
            response.raise_for_status()
            response_content = response.content
            write_repository_zip_backup_to_s3(
                response_content,
                owner,
                repo_name,
                ext,
                bucket_prefix,
                bucket_name,
                boto3_session,
            )
        except requests.exceptions.HTTPError as error_:
            raise error_
        except:
            raise NotImplementedError(f"Can't catch this error: {response.status_code}")


def get_owner_name(token: str) -> str:
    my_headers = {"Authorization": f"Bearer {token}"}
    response = get_url("https://api.github.com/user", headers=my_headers)
    response_json = response.json()
    username = response_json["login"]
    return username


def get_secret(
    session: boto3.Session,
    secret_name: str,
) -> str:
    region_name = "us-east-1"
    # Create a Secrets Manager client
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        # Decrypts secret using the associated KMS key.
        secret_string = get_secret_value_response["SecretString"]
        secret_dict = eval(secret_string)
        secret = secret_dict[secret_name]
        return secret
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e


if __name__ == "__main__":
    boto3_session = boto3.Session()
    access_token = get_secret(boto3_session, "TOKEN_GITHUB")
    bucket_prefix = get_secret(boto3_session, "BACKUP_S3_PREFIX")
    bucket_name = get_secret(boto3_session, "BACKUP_S3_BUCKET")
    backup_only_owner_repos = get_secret(boto3_session, "BACKUP_ONLY_OWNER_REPOS")

    download_repos(
        access_token,
        backup_only_owner_repos,
        bucket_prefix,
        bucket_name,
        boto3_session,
    )
