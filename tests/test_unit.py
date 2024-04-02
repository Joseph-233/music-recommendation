
import pytest
import requests_mock
from spotify_reco_by_mood_and_pace.main import get_access_token  

@pytest.fixture
def spotify_mock():
    with requests_mock.Mocker() as m:
        m.post("https://accounts.spotify.com/api/token", json={"access_token": "mocked_token", "token_type": "Bearer"})
        yield m

def test_get_access_token_with_mock(spotify_mock):
    access_token = get_access_token()
    assert access_token == "mocked_token", "Should return the mocked access token"
