import sys
sys.path.append('/Users/manuelamiranda/Desktop/music-recommendation')

from mr.streamlit_lib.spotify_integration import setup_spotify_client, get_spotify_data, get_audio_features
from mr.streamlit_lib.data_processing import read_access_token, aggregate_user_profile
from mr.streamlit_lib.utility_functions import run_script, setup_logging
import streamlit as st

# Initialize logging
setup_logging()

# Setup Spotify client
with open("./spotify_reco/models/client_id.txt", "r") as file:
    client_id = file.read().strip()
with open("./spotify_reco/models/client_secret.txt", "r") as file:
    client_secret = file.read().strip()

sp = setup_spotify_client(client_id, client_secret)

# Use the new library functions in your Streamlit app
if st.button("Fetch Spotify Data"):
    access_token = read_access_token("./spotify_reco/models/access_token.txt")
    top_tracks = get_spotify_data(sp, "tracks")
    audio_features_df = get_audio_features(sp, [track['id'] for track in top_tracks])
    user_profile = aggregate_user_profile(audio_features_df)

    if user_profile:
        st.json(user_profile)  # Display the user profile
    else:
        st.error("Failed to fetch Spotify data.")