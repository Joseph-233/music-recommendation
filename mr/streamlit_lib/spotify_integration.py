import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import pandas as pd

def setup_spotify_client(client_id, client_secret):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def get_spotify_data(sp, type="tracks", limit=50):
    url = f"https://api.spotify.com/v1/me/top/{type}"
    headers = {"Authorization": f"Bearer {sp.auth}"}
    response = requests.get(url, headers=headers, params={"limit": limit})
    return response.json()["items"] if response.ok else []

def get_audio_features(sp, track_ids):
    features = sp.audio_features(track_ids)
    return pd.DataFrame(features) if features else pd.DataFrame()