import requests
from dotenv import dotenv_values
import pathlib
import os
import typing


def get_metadata(token: str, path_dir: typing.Union[str, bytes, os.PathLike]) -> list:
        
    my_headers = {'Authorization' : f'Bearer {token}'}
    response = requests.get('https://api.github.com/user/repos', headers=my_headers)
    resp = response.json()
    file_path = path_dir / 'metadata.txt'
    metadata = [{'name':repo['name'],
                  'owner':repo['full_name'].split('/')[0],
                  'is_private':repo['private']} for repo in resp]
    with open(file_path, 'w') as f:
        for line in metadata:
            f.write(str(line)+'\n')
    return metadata 

def download_repos(token: str, dir_name: str='repos/', EXT: str='zip') -> None:
    #EXT  = 'tar'  # it also works
    path_dir = create_dir(dir_name)
    metadata = get_metadata(token, path_dir)
    headers = {
        "Authorization" : f'token {token}',
        "Accept": 'application/vnd.github.v3+json'
    }
    
    REF  = ''      # master/main branch 
    
    full_names = [(repo['owner'], repo['name']) for repo in metadata]

    for owner, repo_name  in full_names:
        url = f'https://api.github.com/repos/{owner}/{repo_name}/{EXT}ball/{REF}'
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
            file_path = path_dir / f'{owner}_{repo_name}.{EXT}'
            with open(file_path, 'wb') as fh:
                fh.write(response.content)
        except requests.exceptions.HTTPError as error_:
            raise error_
        except:
            raise NotImplementedError(f"Can't catch this error: {response.status_code}")

def create_dir(dir_name: str) -> str:
    path_dir = pathlib.Path(dir_name)
    path_dir.mkdir(parents=True, exist_ok=True)
    print(type(path_dir))
    return path_dir
    
    
def main():
    secrets = dotenv_values(".env")
    access_token = secrets['github_token']
    download_repos(access_token)

if __name__ == '__main__':
    main()