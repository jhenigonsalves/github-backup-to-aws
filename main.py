import requests
from dotenv import dotenv_values


def get_metadata(token):
    my_headers = {'Authorization' : f'Bearer {token}'}
    response = requests.get('https://api.github.com/user/repos', headers=my_headers)
    resp = response.json()
    metadata = [{'name':repo['name'],
                  'full_name':repo['full_name'],
                  'is_private':repo['private']} for repo in resp]
    with open('repos/metadata.txt', 'w') as f:
        for line in metadata:
            f.write(str(line)+'\n')
    return metadata 

def download_repos(token, EXT='zip'):
    #EXT  = 'tar'  # it also works
    
    metadata = get_metadata(token)
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
            with open(f'repos/{repo_name}.{EXT}', 'wb') as fh:
                fh.write(response.content)
        except requests.exceptions.HTTPError as error_:
            raise error_
        except:
            raise NotImplementedError(f"Can't catch this error: {response.status_code}")


def main():
    secrets = dotenv_values(".env")
    access_token = secrets['github_token']
    download_repos(access_token)

if __name__ == '__main__':
    main()