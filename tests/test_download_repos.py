import pytest
from unittest.mock import patch, MagicMock
from requests.models import HTTPError

from main import download_repos

# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.


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
        download_repos(token="", backup_only_owner_repos="true", bucket_prefix="")
