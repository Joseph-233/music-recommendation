import pytest
import requests_mock
from streamlit.spotify_auth import get_access_token

@pytest.fixture
def spotify_mock():
    with requests_mock.Mocker() as m:
        m.post(
            "https://accounts.spotify.com/api/token",
            json={"access_token": "mocked_access_token", "token_type": "Bearer", "expires_in": 3600},
            status_code=200
        )
        yield m

def test_get_access_token_with_mock(spotify_mock):
    # This simulates the code you'd get from Spotify after user authorization
    mock_auth_code = "mock_auth_code"
    
    # Call the get_access_token function with the mock_auth_code
    access_token = get_access_token(mock_auth_code)
    
    # Assert to make sure that the access token received from get_access_token is the mocked one
    assert access_token == "mocked_access_token", "Should return the mocked access token"
