from unittest.mock import patch, MagicMock

from main import get_url


# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.


@patch("requests.get")
def test_get_url(mock_requests_get):
    mock_url = "foo"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.url = mock_url

    mock_requests_get.return_value = mock_response
    mocked_request = get_url(mock_url)
    mock_requests_get.assert_called_once()
    assert mocked_request.status_code == 200
    assert mocked_request.url == "foo"


@patch("requests.get")
def test_get_url_with_params(mock_requests_get):
    mock_url = "foo"
    mock_headers = {"foo": "bar"}
    mock_params = {"foo": "bar"}

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.url = "foo"

    mock_requests_get.return_value = mock_response
    mocked_request = get_url(url=mock_url, headers=mock_headers, params=mock_params)
    mock_requests_get.assert_called_once()
    assert mocked_request.status_code == 200
    assert mocked_request.url == "foo"
