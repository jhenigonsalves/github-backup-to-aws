from typing import Dict, List
import requests
from dotenv import dotenv_values
import pathlib

import json


def filter_repository_by_owner(
    repositories: List[Dict],
    owner_name: str = None,
    apply_filter: bool = False,
) -> List[Dict]:
    """
    Receive repositories and filter them by owner_name. Return the subset of repositories filtered.
    If apply_filter = False, return repositories as is.
    """
    if not owner_name:
        return repositories
    elif not apply_filter:
        return repositories
    else:
        repos_filter_by_owner = [
            repo for repo in repositories if repo["owner"] == owner_name
        ]
        return repos_filter_by_owner


def get_metadata(
    token: str, path_dir: pathlib.Path, owner_name: str = None, pages: int = 15
) -> list:
    session = requests.Session()
    metadata = []
    max_per_page = 100  # Max value accepted by github api

    my_headers = {"Authorization": f"Bearer {token}"}

    for page in range(1, pages):
        params = {"per_page": max_per_page, "page": page}
        response = session.get(
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

    metadata = filter_repository_by_owner(metadata, owner_name, apply_filter=True)

    file_path = path_dir / "metadata.json"
    with open(file_path, "w") as outfile:
        json.dump(metadata, outfile)
    return metadata


def download_repos(
    token: str, owner_name: str = None, dir_name: str = "repos/", EXT: str = "zip"
) -> None:
    # EXT  = 'tar'  # it also works
    path_dir = create_dir(dir_name)
    metadata = get_metadata(token, path_dir, owner_name)
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    REF = ""  # master/main branch

    full_names = [(repo["owner"], repo["name"]) for repo in metadata]

    for owner, repo_name in full_names:
        url = f"https://api.github.com/repos/{owner}/{repo_name}/{EXT}ball/{REF}"
        response = requests.get(url, headers=headers)
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


secrets = dotenv_values(".env")
access_token = secrets["github_token"]

owner_name = "jhenigonsalves"
download_repos(access_token, owner_name)
