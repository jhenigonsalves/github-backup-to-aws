import pathlib
from unittest.mock import patch, MagicMock, mock_open

from main import get_metadata


# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.


@patch("main.write_json")
@patch("main.get_url")
@patch("main.filter_repository_by_owner")
def test_is_get_metadata_not_executing_while_loop_if_response_empty(
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
def test_is_get_metadata_if_statment_true(
    # mock_repositories,
    mock_requests_get,
    mock_write_json,
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

    mock_write_json.return_value = None

    foo_path = pathlib.Path("foo_path")
    get_metadata("foo_token", foo_path, "false")
    assert mock_requests_get.call_count == 3


@patch("main.write_json")
@patch("main.get_url")
def test_is_get_metadata_returning_a_dict(
    # mock_repositories,
    mock_requests_get,
    mock_write_json,
):
    side_effect_1 = [
        {
            "id": 1296269,
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "private": "false",
        },
    ]
    side_effect_2 = []

    mock1 = MagicMock()
    mock1.json.return_value = side_effect_1
    mock2 = MagicMock()
    mock2.json.return_value = side_effect_2

    mock_requests_get.side_effect = [mock1, mock2]

    mock_write_json.return_value = None

    foo_path = pathlib.Path("foo_path")
    mocked_metadata = get_metadata("foo_token", foo_path, "false")

    assert mock_requests_get.call_count == 2
    assert len(mocked_metadata) == 1
    assert type(mocked_metadata) == list
    assert type(mocked_metadata[0]) == dict
    assert "name" in mocked_metadata[0].keys()
    assert "owner" in mocked_metadata[0].keys()
    assert "is_private" in mocked_metadata[0].keys()
