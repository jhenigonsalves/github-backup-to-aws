from unittest.mock import patch

from main import filter_repository_by_owner


# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.


@patch("main.get_owner_name")
def test_filter_repository_by_owner_false(mock_owner_name):
    mock_owner_name.return_value = "octocat"
    repositories = [
        {"name": "archive", "owner": "octocat", "is_private": True},
        {"name": "file", "owner": "github_user", "is_private": True},
    ]
    repositories_returned = filter_repository_by_owner(repositories, "false")

    owners = set([dict_["owner"] for dict_ in repositories_returned])
    assert len(owners) > 1
    assert "octocat" in owners
    assert "github_user" in owners
    mock_owner_name.assert_not_called()


@patch("main.get_owner_name")
def test_filter_repository_by_owner_true(mock_owner_name):
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
