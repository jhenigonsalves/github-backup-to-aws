from freezegun import freeze_time
from main import get_prefix

# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.


@freeze_time("2022-03-03")
def test_get_prefix():
    bucket_prefix = "my-prefix"
    generated_prefix = get_prefix(bucket_prefix)

    assert generated_prefix == f"{bucket_prefix}/2022-03-03"
