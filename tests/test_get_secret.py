from unittest.mock import patch, Mock

from main import get_secret


# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.


@patch("boto3.Session")
def test_get_secret_return_values(mock_session):
    mock_session_object = Mock()
    mock_client = Mock()
    mock_client.get_secret_value.return_value = {
        "SecretString": """{"TOKEN_GITHUB":"foo_github_token",
                            "BACKUP_ONLY_OWNER_REPOS":"False",
                            "BACKUP_S3_BUCKET":"foo_bucket_name",
                            "BACKUP_S3_PREFIX":"foo_bucket_prefox"}""",
    }
    mock_session_object.client.return_value = mock_client
    mock_session.return_value = mock_session_object
    secrets = get_secret(mock_session_object, "foo_secret_name")
    assert type(secrets) == dict
    assert secrets["TOKEN_GITHUB"] == "foo_github_token"
    assert secrets["BACKUP_ONLY_OWNER_REPOS"] == "False"
    assert secrets["BACKUP_S3_BUCKET"] == "foo_bucket_name"
    assert secrets["BACKUP_S3_PREFIX"] == "foo_bucket_prefox"
