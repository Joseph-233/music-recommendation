
import pytest
import requests_mock
from spotify_reco_by_mood_and_pace import get_access_token  
import os

@pytest.fixture
def spotify_mock():
    with requests_mock.Mocker() as m:
        m.post("https://accounts.spotify.com/api/token", json={"access_token": "mocked_token", "token_type": "Bearer"})
        yield m

def test_get_access_token_with_mock(spotify_mock):
    access_token = get_access_token()
    assert access_token == "mocked_token", "Should return the mocked access token"
# Assuming get_access_token uses these environment variables

def test_spotify_credentials():
    # Retrieve environment variables
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # Check if the environment variables are not None
    assert client_id is not None, "SPOTIFY_CLIENT_ID is not set."
    assert client_secret is not None, "SPOTIFY_CLIENT_SECRET is not set."

