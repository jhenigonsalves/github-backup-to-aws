import pytest
from unittest.mock import patch, MagicMock
from requests.models import HTTPError

from main import download_repos


# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.
@patch("main.get_metadata")
@patch("main.get_url")
@patch("main.write_repository_zip_backup_to_s3")
def test_download_repos_empty_metadata(
    mock_write_repository_zip_backup_to_s3,
    mock_get_url,
    mock_metadata,
):
    mock_metadata.return_value = []
    mock_get_url.return_value = None
    mock_write_repository_zip_backup_to_s3.return_value = None

    download_repos(
        "foo_token",
        "foo_bool",
        "foo_prefix",
        "foo_bucket_name",
        "foo_boto3",
    )

    mock_metadata.assert_called_once()
    mock_get_url.call_count == 0
    mock_write_repository_zip_backup_to_s3.call_count == 0


@patch("main.get_metadata")
@patch("main.get_url")
def test_download_repos_raise_http_error(patch_get_url, p_get_metadata):
    p_get_metadata.return_value = [
        {
            "id": 1296269,
            "name": "Hello-World",
            "owner": "foo",
        },
    ]

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = HTTPError
    patch_get_url.return_value = mock_response

    with pytest.raises(HTTPError):
        download_repos(
            token="",
            backup_only_owner_repos="true",
            bucket_prefix="",
            bucket_name="",
            boto3_session="",
        )


@patch("main.get_metadata")
@patch("main.get_url")
@patch("main.write_repository_zip_backup_to_s3")
def test_download_repos_raise_not_implemented_error(
    mock_write_repository_zip_backup_to_s3,
    mock_get_url,
    mock_metadata,
):
    mock_metadata.return_value = [
        {"name": "archive", "owner": "octocat", "is_private": True},
    ]

    mock_write_repository_zip_backup_to_s3.return_value = None

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.side_effect = EOFError
    mock_get_url.return_value = mock_response

    with pytest.raises(NotImplementedError):
        download_repos(
            token="",
            backup_only_owner_repos="true",
            bucket_prefix="",
            bucket_name="",
            boto3_session="",
        )

    mock_metadata.assert_called_once()
    mock_get_url.call_count == 1
    mock_write_repository_zip_backup_to_s3.call_count == 0


@patch("main.get_metadata")
@patch("main.get_url")
@patch("main.write_repository_zip_backup_to_s3")
def test_download_repos_succes(
    mock_write_repository_zip_backup_to_s3,
    mock_get_url,
    mock_metadata,
):
    mock_metadata.return_value = [
        {"name": "archive", "owner": "octocat", "is_private": True},
        {"name": "file", "owner": "github_user", "is_private": True},
    ]

    mock_response = MagicMock()
    mock_response.status_code = 302
    mock_response.json.return_value = None
    mock_get_url.return_value = mock_response
    mock_write_repository_zip_backup_to_s3.return_value = None

    download_repos(
        "foo_token",
        "foo_bool",
        "foo_prefix",
        "foo_bucket_name",
        "foo_boto3",
    )

    mock_metadata.assert_called_once()
    mock_get_url.call_count == 2
    mock_write_repository_zip_backup_to_s3.call_count == 2
