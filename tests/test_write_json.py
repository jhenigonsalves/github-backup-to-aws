from unittest.mock import patch, mock_open, MagicMock
import pathlib

from main import write_json


@patch("json.dumps", MagicMock(return_values="{cool}"))
@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_write_json(mock_file_open, mock_json_dump):
    mock_json_dump.return_value = {"mcok_key": "mock_value"}

    foo_path = pathlib.Path("foo")
    write_json(mock_json_dump, foo_path)
    assert open("path/to/open").read() == "data"
    mock_file_open.assert_called_with("path/to/open")


@patch("json.dumps", MagicMock(return_values="{cool}"))
@patch("builtins.open", new_callable=mock_open, read_data="data")
@patch("main.get_url")
@patch("main.filter_repository_by_owner")
def test_get_metadata_file_write(
    mock_repositories,
    mock_requests_get,
    mock_file,  # mock_json_dumps
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {},
    ]

    mock_requests_get.return_value = mock_response

    mock_repositories.return_value = [
        {"name": "archive", "owner": "octocat", "is_private": True},
        {"name": "file", "owner": "github_user", "is_private": True},
    ]

    assert open("path/to/open").read() == "data"
    mock_file.assert_called_with("path/to/open")
    mock_requests_get.assert_called_once()
    mock_repositories.assert_called_once()
