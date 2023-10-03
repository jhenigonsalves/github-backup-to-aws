import requests
from dotenv import dotenv_values
import pathlib

def get_metadata(token, path_dir):
        
    my_headers = {'Authorization' : f'Bearer {token}'}
    response = requests.get('https://api.github.com/user/repos', headers=my_headers)
    resp = response.json()
    file_path = path_dir / 'metadata.txt'
    metadata = [{'name':repo['name'],
                  'full_name':repo['full_name'],
                  'is_private':repo['private']} for repo in resp]
    with open(file_path, 'w') as f:
        for line in metadata:
            f.write(str(line)+'\n')
    return metadata 

def download_repos(token, path_dir, EXT='zip'):
    #EXT  = 'tar'  # it also works
    
    metadata = get_metadata(token, path_dir)
    headers = {
        "Authorization" : f'token {token}',
        "Accept": 'application/vnd.github.v3+json'
    }
    
    REF  = ''      # master/main branch 
    
    full_names = [repo['full_name'] for repo in metadata]
    for owner_repo  in full_names:
        repo_name = owner_repo.split('/')[-1]
        url = f'https://api.github.com/repos/{owner_repo}/{EXT}ball/{REF}'
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
            file_path = path_dir / f'{repo_name}.{EXT}'
            with open(file_path, 'wb') as fh:
                fh.write(response.content)
        except requests.exceptions.HTTPError as error_:
            raise error_
        except:
            raise NotImplementedError(f"Can't catch this error: {response.status_code}")


def main():
    secrets = dotenv_values(".env")
    access_token = secrets['github_token']
    
    path_dir = pathlib.Path("repos/")
    path_dir.mkdir(parents=True, exist_ok=True)
    
    download_repos(access_token, path_dir)

if __name__ == '__main__':
    main()