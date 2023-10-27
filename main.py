from typing import Dict, List
import requests
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry
import pathlib
import os
import json

# Api Call Restrictions
period_in_seconds = 60
calls_per_period = 30


def filter_repository_by_owner(
    repositories: List[Dict],
    backup_only_owner_repos: str = None,
    token: str = None,
) -> List[Dict]:
    """
    Receive repositories and filter them by owner_name. Return the subset of repositories filtered.
    If apply_filter = False, return repositories as is.
    """
    if backup_only_owner_repos:
        owner_name = get_owner_name(token)
        repos_filter_by_owner = [
            repo for repo in repositories if repo["owner"] == owner_name
        ]
        return repos_filter_by_owner
    return repositories


def get_metadata(
    token: str,
    path_dir: pathlib.Path,
    backup_only_owner_repos: str = "",
    pages: int = 15,
) -> list:
    metadata = []
    max_per_page = 100  # Max value accepted by github api

    my_headers = {"Authorization": f"Bearer {token}"}
    for page in range(1, pages):
        params = {"per_page": max_per_page, "page": page}
        response = get_url(
            "https://api.github.com/user/repos", headers=my_headers, params=params
        )
        response_json = response.json()
        if len(response_json) != 0:
            aux_metadata = [
                {
                    "name": repo["name"],
                    "owner": repo["full_name"].split("/")[0],
                    "is_private": repo["private"],
                }
                for repo in response_json
            ]
            metadata = metadata + aux_metadata
        else:
            break

    metadata = filter_repository_by_owner(metadata, backup_only_owner_repos, token)

    file_path = path_dir / "metadata.json"
    with open(file_path, "w") as outfile:
        json.dump(metadata, outfile)
    return metadata


@sleep_and_retry
@limits(calls=calls_per_period, period=period_in_seconds)
def get_url(url: str, headers: Dict = {}, params: Dict = {}):
    if params:
        return requests.get(url, headers=headers, params=params)
    return requests.get(url, headers=headers)


def download_repos(
    token: str,
    backup_only_owner_repos: bool,
    dir_name: str = "repos/",
    EXT: str = "zip",
) -> None:
    # EXT  = 'tar'  # it also works

    path_dir = create_dir(dir_name)
    metadata = get_metadata(token, path_dir, backup_only_owner_repos)
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    REF = ""  # master/main branch

    full_names = [(repo["owner"], repo["name"]) for repo in metadata]

    for owner, repo_name in full_names:
        url = f"https://api.github.com/repos/{owner}/{repo_name}/{EXT}ball/{REF}"
        response = get_url(url, headers=headers)
        try:
            response.raise_for_status()
            file_path = path_dir / f"{owner}_{repo_name}.{EXT}"
            with open(file_path, "wb") as fh:
                fh.write(response.content)
        except requests.exceptions.HTTPError as error_:
            raise error_
        except:
            raise NotImplementedError(f"Can't catch this error: {response.status_code}")


def create_dir(dir_name: str) -> str:
    path_dir = pathlib.Path(dir_name)
    path_dir.mkdir(parents=True, exist_ok=True)
    return path_dir


def get_owner_name(token: str) -> str:
    my_headers = {"Authorization": f"Bearer {token}"}
    response = get_url("https://api.github.com/user", headers=my_headers)
    response_json = response.json()
    username = response_json["login"]
    return username


if __name__ == "__main__":
    load_dotenv()
    access_token = os.environ["TOKEN_GITHUB"]
    backup_only_owner_repos = os.environ.get("BACKUP_ONLY_OWNER_REPOS", None)
    download_repos(access_token, backup_only_owner_repos)
