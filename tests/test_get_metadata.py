import pathlib
from unittest.mock import patch, MagicMock

from main import get_metadata
import pytest

# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.


@patch("main.get_url")
@patch("main.filter_repository_by_owner")
@patch("json.dumps")
@patch("main.write_metadata_in_s3_bucket")
def test_is_get_metadata_not_executing_while_loop_if_response_empty(
    mock_repositories,
    mock_requests_get,
    mock_json_dumps,
    mock_write_metadata,
):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_requests_get.return_value = mock_response
    mock_json_dumps.return_value = None
    mock_repositories.return_value = None
    mock_write_metadata.return_vaue = None

    get_metadata(
        "foo_token",
        "false",
        "foo_prefix",
        "foo_bucket_name",
    )

    mock_requests_get.assert_called_once()


@patch("main.get_url")
@patch("json.dumps")
@patch("main.write_metadata_in_s3_bucket")
def test_is_get_metadata_while_loop_executing(
    mock_write_metadata,
    mock_json_dumps,
    mock_requests_get,
):
    side_effect_1 = [
        {
            "id": 1296269,
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "private": "false",
        },
    ]
    side_effect_2 = [
        {
            "id": 1296262349,
            "name": "Hello",
            "full_name": "octocat/Hello",
            "private": "false",
        },
    ]
    side_effect_3 = []

    mock1 = MagicMock()
    mock1.json.return_value = side_effect_1
    mock2 = MagicMock()
    mock2.json.return_value = side_effect_2
    mock3 = MagicMock()
    mock3.json.return_value = side_effect_3
    mock_requests_get.side_effect = [mock1, mock2, mock3]

    mock_json_dumps.return_value = None
    mock_write_metadata.return_vaue = None

    get_metadata(
        "foo_token",
        "false",
        "foo_prefix",
        "foo_bucket_name",
    )
    assert mock_requests_get.call_count == 3


@patch("main.get_url")
@patch("main.filter_repository_by_owner")
@patch("json.dumps")
@patch("main.write_metadata_in_s3_bucket")
def test_is_get_metadata_calling_filter_repository_by_owner(
    mock_write_metadata,
    mock_json_dumps,
    mock_repositories,
    mock_requests_get,
):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_requests_get.return_value = mock_response
    mock_json_dumps.return_value = None
    mock_repositories.return_value = None
    mock_write_metadata.return_vaue = None

    get_metadata(
        "foo_token",
        "false",
        "foo_prefix",
        "foo_bucket_name",
    )

    mock_repositories.assert_called_once()


@patch("main.get_url")
@patch("json.dumps")
@patch("main.write_metadata_in_s3_bucket")
def test_is_get_metadata_returning_a_list_of_dicts(
    mock_write_metadata_in_s3_bucket,
    mock_json_dumps,
    mock_requests_get,
):
    side_effect_1 = [
        {
            "id": 1296269,
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "private": "false",
        },
    ]
    side_effect_2 = [
        {
            "id": 1296262349,
            "name": "Hello",
            "full_name": "octocat/Hello",
            "private": "false",
        },
    ]
    side_effect_3 = []

    mock1 = MagicMock()
    mock1.json.return_value = side_effect_1
    mock2 = MagicMock()
    mock2.json.return_value = side_effect_2
    mock3 = MagicMock()
    mock3.json.return_value = side_effect_3
    mock_requests_get.side_effect = [mock1, mock2, mock3]
    mock_json_dumps.return_value = None
    mock_write_metadata_in_s3_bucket.return_value = None

    mocked_metadata = get_metadata(
        "foo_token",
        "false",
        "foo_prefix",
        "foo_bucket_name",
    )

    assert mock_requests_get.call_count == 3
    assert len(mocked_metadata) == 2
    assert type(mocked_metadata) == list
    assert type(mocked_metadata[0]) == dict
    assert "name" in mocked_metadata[0].keys()
    assert "owner" in mocked_metadata[0].keys()
    assert "is_private" in mocked_metadata[0].keys()
