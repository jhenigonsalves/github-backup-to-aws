import requests
from dotenv import dotenv_values


def get_metadados(token):
    my_headers = {'Authorization' : f'Bearer {token}'}
    response = requests.get('https://api.github.com/user/repos', headers=my_headers)
    resp = response.json()
    metadados = [{'name':repo['name'],
                  'full_name':repo['full_name'],
                  'is_private':repo['private']} for repo in resp]
    with open('repos/metadados.txt', 'w') as f:
        for line in metadados:
            f.write(str(line)+'\n')
    return metadados 

def download_repos(token, EXT='zip'):
    #EXT  = 'tar'  # it also works
    
    metadados = get_metadados(token)
    headers = {
        "Authorization" : f'token {token}',
        "Accept": 'application/vnd.github.v3+json'
    }
    
    REF  = ''      # master/main branch 
    
    
    
    full_names = [repo['full_name'] for repo in metadados]
    for owner_repo  in full_names:
        repo_name = owner_repo.split('/')[-1]
        url = f'https://api.github.com/repos/{owner_repo}/{EXT}ball/{REF}'
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            with open(f'repos/{repo_name}.{EXT}', 'wb') as fh:
                fh.write(r.content)
        else:
            print(repo_name)
            print(url)        
            print(r.text)
def main():
    secrets = dotenv_values(".env")
    access_token = secrets['github_token']
    #access_token_30 = secrets['github_token_30']   
    download_repos(access_token)

if __name__ == '__main__':
    main()