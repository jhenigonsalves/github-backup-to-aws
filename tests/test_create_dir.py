from unittest.mock import patch, MagicMock

from main import create_dir


# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.
@patch("pathlib.Path.mkdir", autospec=True)
def test_create_dir(pathlib_mkdir):
    pathlib_mkdir.return_value = True
    create_dir("tmpdir")
    pathlib_mkdir.assert_called_once()
