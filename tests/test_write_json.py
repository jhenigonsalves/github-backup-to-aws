from unittest.mock import patch, mock_open, MagicMock
import pathlib

from main import write_json


@patch("json.dump")
@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_write_json(mock_file_open, mock_json_dump):
    mock_dict = {"mock_key": "mock_value"}
    mock_json_dump.return_value = mock_dict

    foo_path = pathlib.Path("foo")
    write_json(mock_dict, foo_path)
    assert open("foo").read() == "data"
    mock_file_open.assert_called_with("foo")
    mock_json_dump.assert_called_once()
