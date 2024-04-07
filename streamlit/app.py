# IMPORTANT: Run this in console "streamlit run streamlit\app.py"

from pathlib import Path
import sys

import streamlit as st
import streamlit.components.v1 as components
import subprocess, os
import pandas as pd
import requests
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sys.path.append(str(Path(__file__).resolve().parent.parent))
from spotify_reco.models import predict_features_by_tempo

# Set up Spotify client
with open("streamlit/spotify_credential/client_id.txt", "r") as file:
    client_id = file.read().strip()
with open("streamlit/spotify_credential/client_secret.txt", "r") as file:
    client_secret = file.read().strip()
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",
    format="%(name)s - %(levelname)s - %(message)s",
)

# Add a title and some text to your app
st.title("Spotify Running Recomender")
st.write(
    "This is a streamlit application that leverages a recommendation model that takes into account your Spotify data and recommends songs based on the heart rate number provided. Hopefully it can help you find the perfect playlist for your next run."
)

# The path to spotify_auth.py from the streamlit folder
script_path = "streamlit/spotify_auth.py"

# Add a button to run the spotify_auth.py script
if st.button("Authorize Spotify"):
    # This will run your spotify_auth.py script located in the spotify_reco directory
    result = subprocess.run(
        ["python", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # You can display the output or error to the Streamlit app if you want
    if result.returncode == 0:
        # If the script ran successfully
        st.success("Authorization successful!")
        # st.code(result.stdout)
    else:
        # If the script failed
        st.error("Authorization failed.")
        # st.code(result.stderr)


# Function to encapsulate the process of fetching and displaying Spotify user data
def fetch_and_display_spotify_user_data(file_path):

    def read_access_token(file_path):
        with open(file_path, "r") as file:
            return file.read().strip()

    # Nested function to get Spotify top data
    def get_spotify_top_data(access_token, data_type="tracks", limit=50):
        url = f"https://api.spotify.com/v1/me/top/{data_type}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers, params={"limit": limit})

        if response.status_code == 200:
            items = response.json()["items"]
            return [item["id"] for item in items], [item for item in items]
        else:
            print(f"Error fetching top {data_type}: {response.status_code}")
            return [], []

    # Nested function to fetch audio features
    def fetch_audio_features(track_ids, access_token):
        url = "https://api.spotify.com/v1/audio-features"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            url, headers=headers, params={"ids": ",".join(track_ids)}
        )

        if response.status_code == 200:
            return response.json()["audio_features"]
        else:
            print(f"Error fetching audio features: {response.status_code}")
            return []

    # Nested function to aggregate user profile
    def aggregate_user_profile(audio_features):
        # Convert the list of audio features into a DataFrame
        features_df = pd.DataFrame(audio_features)

        # Select relevant features for aggregation
        relevant_features = [
            "danceability",
            "energy",
            "valence",
            "tempo",
            "acousticness",
            "instrumentalness",
            "speechiness",
            "liveness",
        ]
        profile = features_df[relevant_features].mean().to_dict()

        return profile

    # Read access token from file
    access_token = read_access_token(file_path)

    # Fetch top tracks and artists
    top_tracks_ids, top_tracks_items = get_spotify_top_data(access_token, "tracks")
    top_artists_ids, _ = get_spotify_top_data(access_token, "artists")
    st.session_state["top_tracks_ids"] = top_tracks_ids

    # Fetch audio features
    audio_features = fetch_audio_features(top_tracks_ids, access_token)

    # Aggregate user profile
    user_profile = aggregate_user_profile(audio_features)

    return user_profile  # You could return more data if needed


# Example usage in your Streamlit app
if st.button("Fetch Spotify Data"):
    user_profile = fetch_and_display_spotify_user_data(
        "streamlit/spotify_credential/access_token.txt"
    )
    if user_profile:
        # Store user_profile in session state for later use
        st.session_state["user_profile"] = user_profile

        # Displaying fetched Spotify data features
        st.success("Spotify data fetched successfully.")
        st.write("Your Spotify user profile features:")
        st.json(
            user_profile
        )  # Using st.json for a nicely formatted display of the dictionary
    else:
        st.error("Failed to fetch Spotify data.")


st.title("Heart Rate Input:")

# User input for heart rate
st.session_state.heart_rate = st.number_input(
    "Enter your heart rate (bpm)(60-200)", min_value=60, max_value=200
)


def search_track_id(top_10_with_names, reco_num):
    # Search for the track
    print(
        "search reco num:", reco_num, "len(top_10_with_names)", len(top_10_with_names)
    )
    query = (
        "artist:"
        + top_10_with_names.iloc[reco_num]["artist"]
        + " track:"
        + top_10_with_names.iloc[reco_num]["name"]
    )
    results = sp.search(
        q=query,
        type="track",
    )

    # Get the first track from the results
    track = results["tracks"]["items"][0]

    # Get the track ID
    track_id = track["id"]

    return track_id


def show_top_10_recommendations():
    with st.spinner("Fetching top recommendations..."):
        predict_features_by_tempo.load_model()
        features = predict_features_by_tempo.predict_features(
            st.session_state.heart_rate
        )
        top_tracks = st.session_state["top_tracks_ids"][0:5]
        print("top_tracks", top_tracks)
        print(f"Search min tempo: {st.session_state.heart_rate}")
        top_10_with_names = sp.recommendations(
            seed_tracks=top_tracks,
            limit=50,
            target_tempo=st.session_state.heart_rate,
            min_tempo=st.session_state.heart_rate,
            **features,
        )
        if top_10_with_names:
            items = top_10_with_names["tracks"]
            st.session_state.top_10_with_names_df = pd.DataFrame(
                columns=["id", "name", "artist"]
            )
            for item in items:
                track = [item["id"], item["name"], item["artists"][0]["name"]]
                st.session_state.top_10_with_names_df = pd.concat(
                    [
                        st.session_state.top_10_with_names_df,
                        pd.DataFrame([track], columns=["id", "name", "artist"]),
                    ]
                )
        else:
            print(f"Error fetching top 10 reco: {top_10_with_names.status_code}")
        # Display top 10 recommendations with titles and artist names
        if not st.session_state.top_10_with_names_df.empty:
            st.success(
                "Here are your top 10 song recommendations based on your heart rate:"
            )
            st.session_state.top_10_with_names_df.to_csv(
                "streamlit/temp_data/top_10_with_names.csv", index=False
            )
            st.dataframe(st.session_state.top_10_with_names_df)

        else:
            st.write("No recommendations available based on the chosen heart rate.")


st.title("Top 50 Songs for Running:")

if "reco_num" not in st.session_state:
    # record the now playing track
    st.session_state.reco_num = 0

# Button for getting recommendations
if st.button("Get Recommendations"):
    st.session_state.reco_num = 0
    show_top_10_recommendations()


st.title("Listen and Choose:")
# dislike_btn = st.button(":x:", use_container_width=True)
# like_btn = st.button(":heart:", use_container_width=True)
top_10_with_names = pd.read_csv("streamlit/temp_data/top_10_with_names.csv")
if not os.path.exists("streamlit/temp_data/preferences.csv"):
    # Create the file if it doesn't exist
    pd.DataFrame(columns=["track_id", "name", "artist", "preference"]).to_csv(
        "streamlit/temp_data/preferences.csv", index=False
    )
preferences = pd.read_csv("streamlit/temp_data/preferences.csv")
track_id = pd.read_csv("streamlit/temp_data/top_10_with_names.csv").iloc[
    st.session_state.reco_num
]["id"]

if st.button(":x:", use_container_width=True):
    # Find the record
    record = preferences.loc[preferences["track_id"] == track_id]

    if record.empty:
        # If the record is not found, insert a new record
        preferences = pd.concat(
            [
                preferences,
                pd.DataFrame(
                    {
                        "track_id": [track_id],
                        "name": [
                            top_10_with_names.iloc[st.session_state.reco_num]["name"]
                        ],
                        "artist": [
                            top_10_with_names.iloc[st.session_state.reco_num]["artist"]
                        ],
                        "preference": [-1],
                    }
                ),
            ]
        )
    else:
        # If the record is found, update it
        preferences.loc[preferences["track_id"] == track_id, "preference"] = -1
    st.session_state.reco_num += 1


if st.button(":heart:", use_container_width=True):
    # Find the record
    record = preferences.loc[preferences["track_id"] == track_id]

    if record.empty:
        # If the record is not found, insert a new record
        preferences = pd.concat(
            [
                preferences,
                pd.DataFrame(
                    {
                        "track_id": [track_id],
                        "name": [
                            top_10_with_names.iloc[st.session_state.reco_num]["name"]
                        ],
                        "artist": [
                            top_10_with_names.iloc[st.session_state.reco_num]["artist"]
                        ],
                        "preference": [1],
                    }
                ),
            ]
        )
    else:
        # If the record is found, update it
        preferences.loc[preferences["track_id"] == track_id, "preference"] = 1
    st.session_state.reco_num += 1

preferences.to_csv("streamlit/temp_data/preferences.csv", index=False)


def render_listen_and_choose():
    track_id = pd.read_csv("streamlit/temp_data/top_10_with_names.csv").iloc[
        st.session_state.reco_num
    ]["id"]
    # Embed the Spotify iframe in the Streamlit app
    # https://open.spotify.com/embed/track/7rU6Iebxzlvqy5t857bKFq?utm_source=generator&theme=0
    # Create the URL for the Spotify iframe
    components.iframe(
        "https://open.spotify.com/embed/track/"
        + track_id
        + "?utm_source=generator&theme=0",
        width=700,
        height=352,
    )


render_listen_and_choose()
