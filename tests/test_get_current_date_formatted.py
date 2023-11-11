from unittest.mock import patch
from main import get_current_date_formatted
from datetime import date
from datetime import datetime

# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.


@patch("main.date")
def test_get_current_date_format1(mock_datetime_date):
    mock_datetime_date.today.return_value = date(2012, 12, 10)
    mock_datetime_date.side_effect = lambda *args, **kw: date(*args, **kw)
    mocked_date = get_current_date_formatted()

    assert mocked_date == "2012-12-10"
    mock_datetime_date.today.assert_called_once()


@patch("main.date")
def test_get_current_date_format2(mock_datetime_date):
    mock_datetime_date.today.return_value = datetime.strptime("10/12/2012", "%d/%m/%Y")
    mock_datetime_date.side_effect = lambda *args, **kw: date(*args, **kw)
    mocked_date = get_current_date_formatted()

    assert mocked_date == "2012-12-10"
    mock_datetime_date.today.assert_called_once()


@patch("main.date")
def test_get_current_date_format3(mock_datetime_date):
    mock_datetime_date.today.return_value = datetime.strptime(
        "10 December, 2012", "%d %B, %Y"
    )
    mock_datetime_date.side_effect = lambda *args, **kw: date(*args, **kw)
    mocked_date = get_current_date_formatted()

    assert mocked_date == "2012-12-10"
    mock_datetime_date.today.assert_called_once()
