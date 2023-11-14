from main import get_current_date_formatted
from freezegun import freeze_time


# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.
@freeze_time("2022-01-01")
def test_get_current_date_as_formatted_string():
    current_date = get_current_date_formatted()
    assert current_date == "2022-01-01"
