from unittest.mock import patch, MagicMock

from main import create_dir
from main import get_owner_name
from main import filter_repository_by_owner
from main import get_url


# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.
@patch("pathlib.Path.mkdir", autospec=True)
def test_create_dir(pathlib_path):
    pathlib_path.return_value = True
    create_dir("tmpdir")
    pathlib_path.assert_called_once()


@patch("requests.get")
def test_get_owner_name(mock_requests):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "login": "octocat",
        "id": 1,
        "node_id": "MDQ6VXNlcjE=",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "",
        "url": "https://api.github.com/users/octocat",
        "html_url": "https://github.com/octocat",
        "followers_url": "https://api.github.com/users/octocat/followers",
        "following_url": "https://api.github.com/users/octocat/following{/other_user}",
        "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
        "organizations_url": "https://api.github.com/users/octocat/orgs",
        "repos_url": "https://api.github.com/users/octocat/repos",
        "events_url": "https://api.github.com/users/octocat/events{/privacy}",
        "received_events_url": "https://api.github.com/users/octocat/received_events",
        "type": "User",
        "site_admin": "false",
        "name": "monalisa octocat",
        "company": "GitHub",
        "blog": "https://github.com/blog",
        "location": "San Francisco",
        "email": "octocat@github.com",
        "hireable": "false",
        "bio": "There once was...",
        "twitter_username": "monatheoctocat",
        "public_repos": 2,
        "public_gists": 1,
        "followers": 20,
        "following": 0,
        "created_at": "2008-01-14T04:33:35Z",
        "updated_at": "2008-01-14T04:33:35Z",
        "private_gists": 81,
        "total_private_repos": 100,
        "owned_private_repos": 100,
        "disk_usage": 10000,
        "collaborators": 8,
        "two_factor_authentication": "true",
        "plan": {
            "name": "Medium",
            "space": 400,
            "private_repos": 20,
            "collaborators": 0,
        },
    }

    # specify the return value of the get() method
    mock_requests.return_value = mock_response

    owner_name = get_owner_name("")
    assert owner_name == "octocat"


@patch("main.get_owner_name")
def test_filter_repository_by_owner_None(mock_owner_name):
    mock_owner_name.return_value = "octocat"
    repositories = [
        {"name": "archive", "owner": "octocat", "is_private": True},
        {"name": "file", "owner": "github_user", "is_private": True},
    ]
    repositories_returned = filter_repository_by_owner(repositories)

    owners = set([dict_["owner"] for dict_ in repositories_returned])
    assert len(owners) > 1
    assert "octocat" in owners
    assert "github_user" in owners
    mock_owner_name.assert_not_called()


@patch("main.get_owner_name")
def test_filter_repository_by_owner_True(mock_owner_name):
    mock_owner_name.return_value = "octocat"
    repositories = [
        {"name": "archive", "owner": "octocat", "is_private": True},
        {"name": "file", "owner": "github_user", "is_private": True},
    ]
    repositories_returned = filter_repository_by_owner(repositories, "True")

    owners = set([dict_["owner"] for dict_ in repositories_returned])
    assert len(owners) == 1
    assert "octocat" in owners
    assert "github_user" not in owners
    mock_owner_name.assert_called_once()


@patch("requests.get")
def test_get_url(mock_requests):
    mock_url = "foo"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.url = mock_url

    mock_requests.return_value = mock_response
    mocked_request = get_url(mock_url)
    mock_requests.assert_called_once()
    assert mocked_request.status_code == 200
    assert mocked_request.url == "foo"
