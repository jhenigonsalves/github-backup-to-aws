import pathlib
from unittest.mock import patch, MagicMock, mock_open

from main import get_metadata


# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.


# @patch("main.filter_repository_by_owner")
# @patch("main.get_url")
# def test_get_metadata(mock_requests, mock_file):
#     mock_response = MagicMock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = [
#         {
#             "id": 1296269,
#             "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
#             "name": "Hello-World",
#             "full_name": "octocat/Hello-World",
#             "owner": {
#                 "login": "octocat",
#                 "id": 1,
#                 "node_id": "MDQ6VXNlcjE=",
#                 "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#                 "gravatar_id": "",
#                 "url": "https://api.github.com/users/octocat",
#                 "html_url": "https://github.com/octocat",
#                 "followers_url": "https://api.github.com/users/octocat/followers",
#                 "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#                 "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#                 "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#                 "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#                 "organizations_url": "https://api.github.com/users/octocat/orgs",
#                 "repos_url": "https://api.github.com/users/octocat/repos",
#                 "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#                 "received_events_url": "https://api.github.com/users/octocat/received_events",
#                 "type": "User",
#                 "site_admin": "false",
#             },
#             "private": "false",
#             "html_url": "https://github.com/octocat/Hello-World",
#             "description": "This your first repo!",
#             "fork": "false",
#             "url": "https://api.github.com/repos/octocat/Hello-World",
#             "archive_url": "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
#             "assignees_url": "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
#             "blobs_url": "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
#             "branches_url": "https://api.github.com/repos/octocat/Hello-World/branches{/branch}",
#             "collaborators_url": "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
#             "comments_url": "https://api.github.com/repos/octocat/Hello-World/comments{/number}",
#             "commits_url": "https://api.github.com/repos/octocat/Hello-World/commits{/sha}",
#             "compare_url": "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
#             "contents_url": "https://api.github.com/repos/octocat/Hello-World/contents/{+path}",
#             "contributors_url": "https://api.github.com/repos/octocat/Hello-World/contributors",
#             "deployments_url": "https://api.github.com/repos/octocat/Hello-World/deployments",
#             "downloads_url": "https://api.github.com/repos/octocat/Hello-World/downloads",
#             "events_url": "https://api.github.com/repos/octocat/Hello-World/events",
#             "forks_url": "https://api.github.com/repos/octocat/Hello-World/forks",
#             "git_commits_url": "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
#             "git_refs_url": "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
#             "git_tags_url": "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
#             "git_url": "git:github.com/octocat/Hello-World.git",
#             "issue_comment_url": "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
#             "issue_events_url": "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
#             "issues_url": "https://api.github.com/repos/octocat/Hello-World/issues{/number}",
#             "keys_url": "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
#             "labels_url": "https://api.github.com/repos/octocat/Hello-World/labels{/name}",
#             "languages_url": "https://api.github.com/repos/octocat/Hello-World/languages",
#             "merges_url": "https://api.github.com/repos/octocat/Hello-World/merges",
#             "milestones_url": "https://api.github.com/repos/octocat/Hello-World/milestones{/number}",
#             "notifications_url": "https://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}",
#             "pulls_url": "https://api.github.com/repos/octocat/Hello-World/pulls{/number}",
#             "releases_url": "https://api.github.com/repos/octocat/Hello-World/releases{/id}",
#             "ssh_url": "git@github.com:octocat/Hello-World.git",
#             "stargazers_url": "https://api.github.com/repos/octocat/Hello-World/stargazers",
#             "statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
#             "subscribers_url": "https://api.github.com/repos/octocat/Hello-World/subscribers",
#             "subscription_url": "https://api.github.com/repos/octocat/Hello-World/subscription",
#             "tags_url": "https://api.github.com/repos/octocat/Hello-World/tags",
#             "teams_url": "https://api.github.com/repos/octocat/Hello-World/teams",
#             "trees_url": "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
#             "clone_url": "https://github.com/octocat/Hello-World.git",
#             "mirror_url": "git:git.example.com/octocat/Hello-World",
#             "hooks_url": "https://api.github.com/repos/octocat/Hello-World/hooks",
#             "svn_url": "https://svn.github.com/octocat/Hello-World",
#             "homepage": "https://github.com",
#             "language": "null",
#             "forks_count": 9,
#             "stargazers_count": 80,
#             "watchers_count": 80,
#             "size": 108,
#             "default_branch": "master",
#             "open_issues_count": 0,
#             "is_template": "true",
#             "topics": ["octocat", "atom", "electron", "api"],
#             "has_issues": "true",
#             "has_projects": "true",
#             "has_wiki": "true",
#             "has_pages": "false",
#             "has_downloads": "true",
#             "archived": "false",
#             "disabled": "false",
#             "visibility": "public",
#             "pushed_at": "2011-01-26T19:06:43Z",
#             "created_at": "2011-01-26T19:01:12Z",
#             "updated_at": "2011-01-26T19:14:43Z",
#             "permissions": {"admin": "false", "push": "false", "pull": "true"},
#             "allow_rebase_merge": "true",
#             "template_repository": "null",
#             "temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
#             "allow_squash_merge": "true",
#             "allow_auto_merge": "false",
#             "delete_branch_on_merge": "true",
#             "allow_merge_commit": "true",
#             "subscribers_count": 42,
#             "network_count": 0,
#             "license": {
#                 "key": "mit",
#                 "name": "MIT License",
#                 "url": "https://api.github.com/licenses/mit",
#                 "spdx_id": "MIT",
#                 "node_id": "MDc6TGljZW5zZW1pdA==",
#                 "html_url": "https://github.com/licenses/mit",
#             },
#             "forks": 1,
#             "open_issues": 1,
#             "watchers": 1,
#         },
#     ]

#     # specify the return value of the get() method
#     mock_requests.return_value = mock_response
#     foo_path = pathlib.Path("foo_path")
#     mocked_metadata = get_metadata("foo_token", foo_path, "false")


# # @patch("json.dumps", MagicMock(return_values="{cool}"))
# @patch("builtins.open", new_callable=mock_open, read_data="data")
# @patch("main.get_url")
# @patch("main.filter_repository_by_owner")
# def test_get_metadata_file_write(
#     mock_repositories,
#     mock_requests_get,
#     mock_file,  # mock_json_dumps
# ):
#     mock_response = MagicMock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = [
#         {
#             "id": 1296269,
#             "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
#             "name": "Hello-World",
#             "full_name": "octocat/Hello-World",
#             "owner": {
#                 "login": "octocat",
#                 "id": 1,
#                 "node_id": "MDQ6VXNlcjE=",
#                 "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#                 "gravatar_id": "",
#                 "url": "https://api.github.com/users/octocat",
#                 "html_url": "https://github.com/octocat",
#                 "followers_url": "https://api.github.com/users/octocat/followers",
#                 "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#                 "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#                 "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#                 "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#                 "organizations_url": "https://api.github.com/users/octocat/orgs",
#                 "repos_url": "https://api.github.com/users/octocat/repos",
#                 "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#                 "received_events_url": "https://api.github.com/users/octocat/received_events",
#                 "type": "User",
#                 "site_admin": "false",
#             },
#             "private": "false",
#             "html_url": "https://github.com/octocat/Hello-World",
#             "description": "This your first repo!",
#             "fork": "false",
#             "url": "https://api.github.com/repos/octocat/Hello-World",
#             "archive_url": "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
#             "assignees_url": "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
#             "blobs_url": "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
#             "branches_url": "https://api.github.com/repos/octocat/Hello-World/branches{/branch}",
#             "collaborators_url": "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
#             "comments_url": "https://api.github.com/repos/octocat/Hello-World/comments{/number}",
#             "commits_url": "https://api.github.com/repos/octocat/Hello-World/commits{/sha}",
#             "compare_url": "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
#             "contents_url": "https://api.github.com/repos/octocat/Hello-World/contents/{+path}",
#             "contributors_url": "https://api.github.com/repos/octocat/Hello-World/contributors",
#             "deployments_url": "https://api.github.com/repos/octocat/Hello-World/deployments",
#             "downloads_url": "https://api.github.com/repos/octocat/Hello-World/downloads",
#             "events_url": "https://api.github.com/repos/octocat/Hello-World/events",
#             "forks_url": "https://api.github.com/repos/octocat/Hello-World/forks",
#             "git_commits_url": "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
#             "git_refs_url": "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
#             "git_tags_url": "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
#             "git_url": "git:github.com/octocat/Hello-World.git",
#             "issue_comment_url": "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
#             "issue_events_url": "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
#             "issues_url": "https://api.github.com/repos/octocat/Hello-World/issues{/number}",
#             "keys_url": "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
#             "labels_url": "https://api.github.com/repos/octocat/Hello-World/labels{/name}",
#             "languages_url": "https://api.github.com/repos/octocat/Hello-World/languages",
#             "merges_url": "https://api.github.com/repos/octocat/Hello-World/merges",
#             "milestones_url": "https://api.github.com/repos/octocat/Hello-World/milestones{/number}",
#             "notifications_url": "https://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}",
#             "pulls_url": "https://api.github.com/repos/octocat/Hello-World/pulls{/number}",
#             "releases_url": "https://api.github.com/repos/octocat/Hello-World/releases{/id}",
#             "ssh_url": "git@github.com:octocat/Hello-World.git",
#             "stargazers_url": "https://api.github.com/repos/octocat/Hello-World/stargazers",
#             "statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
#             "subscribers_url": "https://api.github.com/repos/octocat/Hello-World/subscribers",
#             "subscription_url": "https://api.github.com/repos/octocat/Hello-World/subscription",
#             "tags_url": "https://api.github.com/repos/octocat/Hello-World/tags",
#             "teams_url": "https://api.github.com/repos/octocat/Hello-World/teams",
#             "trees_url": "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
#             "clone_url": "https://github.com/octocat/Hello-World.git",
#             "mirror_url": "git:git.example.com/octocat/Hello-World",
#             "hooks_url": "https://api.github.com/repos/octocat/Hello-World/hooks",
#             "svn_url": "https://svn.github.com/octocat/Hello-World",
#             "homepage": "https://github.com",
#             "language": "null",
#             "forks_count": 9,
#             "stargazers_count": 80,
#             "watchers_count": 80,
#             "size": 108,
#             "default_branch": "master",
#             "open_issues_count": 0,
#             "is_template": "true",
#             "topics": ["octocat", "atom", "electron", "api"],
#             "has_issues": "true",
#             "has_projects": "true",
#             "has_wiki": "true",
#             "has_pages": "false",
#             "has_downloads": "true",
#             "archived": "false",
#             "disabled": "false",
#             "visibility": "public",
#             "pushed_at": "2011-01-26T19:06:43Z",
#             "created_at": "2011-01-26T19:01:12Z",
#             "updated_at": "2011-01-26T19:14:43Z",
#             "permissions": {"admin": "false", "push": "false", "pull": "true"},
#             "allow_rebase_merge": "true",
#             "template_repository": "null",
#             "temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
#             "allow_squash_merge": "true",
#             "allow_auto_merge": "false",
#             "delete_branch_on_merge": "true",
#             "allow_merge_commit": "true",
#             "subscribers_count": 42,
#             "network_count": 0,
#             "license": {
#                 "key": "mit",
#                 "name": "MIT License",
#                 "url": "https://api.github.com/licenses/mit",
#                 "spdx_id": "MIT",
#                 "node_id": "MDc6TGljZW5zZW1pdA==",
#                 "html_url": "https://github.com/licenses/mit",
#             },
#             "forks": 1,
#             "open_issues": 1,
#             "watchers": 1,
#         },
#     ]

#     mock_requests_get.return_value = mock_response

#     mock_repositories.return_value = [
#         {"name": "archive", "owner": "octocat", "is_private": True},
#         {"name": "file", "owner": "github_user", "is_private": True},
#     ]

#     assert open("path/to/open").read() == "data"
#     mock_file.assert_called_with("path/to/open")
#     mock_requests_get.assert_called_once()
#     mock_repositories.assert_called_once()


@patch("main.write_json")
@patch("main.get_url")
@patch("main.filter_repository_by_owner")
def test_is_get_metadata_executing_for_loop_at_least_once(
    mock_repositories, mock_requests_get, mock_write_json
):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_requests_get.return_value = mock_response

    mock_repositories.return_value = None
    mock_write_json.return_value = None

    foo_path = pathlib.Path("foo_path")
    get_metadata("foo_token", foo_path, "false")

    mock_requests_get.assert_called_once()


@patch("main.write_json")
@patch("main.get_url")
@patch("main.filter_repository_by_owner")
def test_is_get_metadata_for_loop_breaking_when_response_json_is_empty(
    mock_repositories, mock_requests_get, mock_write_json
):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_requests_get.return_value = mock_response

    mock_repositories.return_value = None
    mock_write_json.return_value = None

    foo_path = pathlib.Path("foo_path")
    get_metadata("foo_token", foo_path, "false")

    assert mock_requests_get.call_count == 1


@patch("main.write_json")
@patch("main.get_url")
@patch("main.filter_repository_by_owner")
def test_is_get_metadata_if_statment_true(
    mock_repositories, mock_requests_get, mock_write_json
):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": 1296269,
            "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "owner": {
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
            },
            "private": "false",
            "html_url": "https://github.com/octocat/Hello-World",
            "description": "This your first repo!",
            "fork": "false",
            "url": "https://api.github.com/repos/octocat/Hello-World",
            "archive_url": "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
            "assignees_url": "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
            "blobs_url": "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
            "branches_url": "https://api.github.com/repos/octocat/Hello-World/branches{/branch}",
            "collaborators_url": "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
            "comments_url": "https://api.github.com/repos/octocat/Hello-World/comments{/number}",
            "commits_url": "https://api.github.com/repos/octocat/Hello-World/commits{/sha}",
            "compare_url": "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
            "contents_url": "https://api.github.com/repos/octocat/Hello-World/contents/{+path}",
            "contributors_url": "https://api.github.com/repos/octocat/Hello-World/contributors",
            "deployments_url": "https://api.github.com/repos/octocat/Hello-World/deployments",
            "downloads_url": "https://api.github.com/repos/octocat/Hello-World/downloads",
            "events_url": "https://api.github.com/repos/octocat/Hello-World/events",
            "forks_url": "https://api.github.com/repos/octocat/Hello-World/forks",
            "git_commits_url": "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
            "git_refs_url": "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
            "git_tags_url": "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
            "git_url": "git:github.com/octocat/Hello-World.git",
            "issue_comment_url": "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
            "issue_events_url": "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
            "issues_url": "https://api.github.com/repos/octocat/Hello-World/issues{/number}",
            "keys_url": "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
            "labels_url": "https://api.github.com/repos/octocat/Hello-World/labels{/name}",
            "languages_url": "https://api.github.com/repos/octocat/Hello-World/languages",
            "merges_url": "https://api.github.com/repos/octocat/Hello-World/merges",
            "milestones_url": "https://api.github.com/repos/octocat/Hello-World/milestones{/number}",
            "notifications_url": "https://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}",
            "pulls_url": "https://api.github.com/repos/octocat/Hello-World/pulls{/number}",
            "releases_url": "https://api.github.com/repos/octocat/Hello-World/releases{/id}",
            "ssh_url": "git@github.com:octocat/Hello-World.git",
            "stargazers_url": "https://api.github.com/repos/octocat/Hello-World/stargazers",
            "statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
            "subscribers_url": "https://api.github.com/repos/octocat/Hello-World/subscribers",
            "subscription_url": "https://api.github.com/repos/octocat/Hello-World/subscription",
            "tags_url": "https://api.github.com/repos/octocat/Hello-World/tags",
            "teams_url": "https://api.github.com/repos/octocat/Hello-World/teams",
            "trees_url": "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
            "clone_url": "https://github.com/octocat/Hello-World.git",
            "mirror_url": "git:git.example.com/octocat/Hello-World",
            "hooks_url": "https://api.github.com/repos/octocat/Hello-World/hooks",
            "svn_url": "https://svn.github.com/octocat/Hello-World",
            "homepage": "https://github.com",
            "language": "null",
            "forks_count": 9,
            "stargazers_count": 80,
            "watchers_count": 80,
            "size": 108,
            "default_branch": "master",
            "open_issues_count": 0,
            "is_template": "true",
            "topics": ["octocat", "atom", "electron", "api"],
            "has_issues": "true",
            "has_projects": "true",
            "has_wiki": "true",
            "has_pages": "false",
            "has_downloads": "true",
            "archived": "false",
            "disabled": "false",
            "visibility": "public",
            "pushed_at": "2011-01-26T19:06:43Z",
            "created_at": "2011-01-26T19:01:12Z",
            "updated_at": "2011-01-26T19:14:43Z",
            "permissions": {"admin": "false", "push": "false", "pull": "true"},
            "allow_rebase_merge": "true",
            "template_repository": "null",
            "temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
            "allow_squash_merge": "true",
            "allow_auto_merge": "false",
            "delete_branch_on_merge": "true",
            "allow_merge_commit": "true",
            "subscribers_count": 42,
            "network_count": 0,
            "license": {
                "key": "mit",
                "name": "MIT License",
                "url": "https://api.github.com/licenses/mit",
                "spdx_id": "MIT",
                "node_id": "MDc6TGljZW5zZW1pdA==",
                "html_url": "https://github.com/licenses/mit",
            },
            "forks": 1,
            "open_issues": 1,
            "watchers": 1,
        },
    ]

    mock_requests_get.return_value = mock_response

    mock_repositories.return_value = None
    mock_write_json.return_value = None

    foo_path = pathlib.Path("foo_path")
    mocked_metadata = get_metadata("foo_token", foo_path, "false")

    assert mock_requests_get.call_count == 1
    assert len(mocked_metadata) == 1
