import pytest
from spotify_reco_by_mood_and_pace import get_access_token  
import time

def test_get_access_token():
    access_token = get_access_token()
    assert isinstance(access_token, str) and len(access_token) > 0, "Access token should be a non-empty string"
