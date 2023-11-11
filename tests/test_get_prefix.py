from unittest.mock import patch

from main import get_prefix

# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.


@patch("main.get_current_date_formatted")
def test_get_prefix(mock_formatted_date):
    mock_formatted_date.return_value = "2012-12-10"
    mocked_prefix = get_prefix("my_prefix")

    assert mocked_prefix == "my_prefix/2012-12-10"
    mock_formatted_date.assert_called_once()
