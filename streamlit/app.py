import streamlit as st
import streamlit.components.v1 as components
import subprocess, os
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
import requests
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify client
with open("./spotify_reco/models/client_id.txt", "r") as file:
    client_id = file.read().strip()
with open("./spotify_reco/models/client_secret.txt", "r") as file:
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
script_path = "../spotify_reco/spotify_auth.py"

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

    # Fetch audio features
    audio_features = fetch_audio_features(top_tracks_ids, access_token)

    # Aggregate user profile
    user_profile = aggregate_user_profile(audio_features)

    return user_profile  # You could return more data if needed


# Example usage in your Streamlit app
if st.button("Fetch Spotify Data"):
    user_profile = fetch_and_display_spotify_user_data(
        "./spotify_reco/models/access_token.txt"
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
heart_rate = st.number_input("Enter your heart rate (bpm)", min_value=0)


def load_data(file_path):
    df = pd.read_csv(file_path)
    # Perform any necessary preprocessing
    return df


# Use the cached load_data function to load your dataset
logging.info("Starting to load data...")
df = load_data("df_streamlit.csv")
logging.info("Data loaded successfully.")


def train_model(df):
    logging.info("Starting model training...")

    # Assuming df is preprocessed and ready for model training
    predictor_columns = [
        "danceability_diff",
        "energy_diff",
        "valence_diff",
        "tempo_diff",
        "acousticness_diff",
        "instrumentalness_diff",
        "speechiness_diff",
        "liveness_diff",
    ]

    try:
        X = df[predictor_columns]
        y = np.log1p(df["play_count"])
        logging.info(
            f"Features and target variable prepared. X shape: {X.shape}, y length: {len(y)}"
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        logging.info("Data split into training and test sets.")

        train_data = lgb.Dataset(X_train, label=y_train)
        test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
        logging.info("LightGBM datasets created.")

        params = {
            "objective": "regression",
            "metric": "rmse",
            "num_leaves": 32,
            "learning_rate": 0.1,
            "feature_fraction": 0.8,
            "bagging_fraction": 0.9,
            "bagging_freq": 5,
            "verbose": -1,
            "max_depth": -1,
            "min_data_in_leaf": 20,
            "lambda_l1": 0.5,
            "lambda_l2": 0.5,
        }

        logging.info("Starting LightGBM training...")
        bst = lgb.train(params, train_data, num_boost_round=100, valid_sets=[test_data])
        logging.info("Model training completed.")

    except Exception as e:
        logging.error(f"Error during model training: {e}", exc_info=True)
        raise e  # Re-raise the exception to handle it in the calling code if necessary

    return bst


def predict_and_display_recommendations(bst, df, user_profile):
    # Apply user_profile to df to calculate differential features
    for feature in user_profile.keys():
        df[f"{feature}_diff"] = abs(df[feature] - user_profile[feature])


def get_top_recommendations(df, model, user_profile, top_n=10):
    # Calculate the differential features based on user_profile
    for feature in user_profile.keys():
        df[f"{feature}_diff"] = abs(df[feature] - user_profile[feature])

    # Prepare the features for prediction
    features = [f"{feature}_diff" for feature in user_profile.keys()]
    # Ensure we only predict for rows that have all required features available
    df_features = df.dropna(subset=features)

    # Predict the play count log for the filtered DataFrame
    predicted_play_count_log = model.predict(df_features[features])

    # Create a DataFrame for predictions
    predictions_df = df_features[["song", "title", "artist_name"]].copy()
    predictions_df["predicted_play_count_log"] = predicted_play_count_log

    # Sort predictions to get top recommendations
    predictions_df = predictions_df.sort_values(
        by="predicted_play_count_log", ascending=False
    )

    # Remove duplicates to ensure unique songs
    top_recommendations = predictions_df.drop_duplicates(subset=["song"]).head(top_n)

    return top_recommendations


def search_track_id(top_10_with_names, reco_num):
    # Search for the track
    print(
        "search reco num:", reco_num, "len(top_10_with_names)", len(top_10_with_names)
    )
    query = (
        "artist:"
        + top_10_with_names.iloc[reco_num]["artist_name"]
        + " track:"
        + top_10_with_names.iloc[reco_num]["title"]
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
        # Load recommended songs from CSV
        recommended_songs = pd.read_csv("recommended_songs.csv")

        # Calculate tempo thirds for the dataset
        tempo_min, tempo_max = (
            recommended_songs["tempo"].min(),
            recommended_songs["tempo"].max(),
        )
        tempo_third = (tempo_max - tempo_min) / 3

        # Determine the desired tempo range based on user-chosen heart rate
        if heart_rate < 100:
            tempo_low, tempo_high = tempo_min, tempo_min + tempo_third
        elif heart_rate <= 140:
            tempo_low, tempo_high = tempo_min + tempo_third, tempo_min + 2 * tempo_third
        else:  # heart_rate > 140
            tempo_low, tempo_high = tempo_min + 2 * tempo_third, tempo_max

        # Filter songs within the desired tempo range
        matching_songs = recommended_songs[
            (recommended_songs["tempo"] >= tempo_low)
            & (recommended_songs["tempo"] <= tempo_high)
        ]

        # Sort remaining songs by predicted play count log, assuming higher is better
        sorted_songs = matching_songs.sort_values(
            by="predicted_play_count_log", ascending=False
        )

        # Extract the top 10 recommendations
        top_10_recommendations = sorted_songs.head(10)

        # Load the dataset_ready2.csv to merge song titles and artist names
        dataset_ready2 = pd.read_csv("dataset_ready2.csv")

        # Merge top_10_recommendations with dataset_ready2 to get song title and artist names
        top_10_with_names = top_10_recommendations.merge(
            dataset_ready2[["song_encoded", "title", "artist_name"]],
            on="song_encoded",
            how="left",
        )

        # Drop duplicates to ensure each song title appears only once
        top_10_with_names = top_10_with_names.drop_duplicates(
            subset="title", keep="first"
        )

        # Display top 10 recommendations with titles and artist names
        if not top_10_with_names.empty:
            st.success(
                "Here are your top 10 song recommendations based on your heart rate:"
            )
            top_10_with_names.to_csv("top_10_with_names.csv", index=False)
            st.dataframe(
                top_10_with_names[["title", "artist_name", "predicted_play_count_log"]]
            )

        else:
            st.write("No recommendations available based on the chosen heart rate.")


st.title("Top 10 Songs for Running:")

if "reco_num" not in st.session_state:
    # record the now playing track
    st.session_state.reco_num = 0

# Button for getting recommendations
if st.button("Get Recommendations"):
    st.session_state.reco_num = 0
    show_top_10_recommendations()


st.title("Listen and Choose:")
dislike_btn = st.button(":x:", use_container_width=True)
like_btn = st.button(":heart:", use_container_width=True)
top_10_with_names = pd.read_csv("top_10_with_names.csv")
if not os.path.exists("preferences.csv"):
    # Create the file if it doesn't exist
    pd.DataFrame(columns=["track_id", "title", "artist", "preference"]).to_csv(
        "preferences.csv", index=False
    )
preferences = pd.read_csv("preferences.csv")
track_id = search_track_id(top_10_with_names, st.session_state.reco_num)

if dislike_btn:
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
                        "title": [top_10_with_names.iloc[st.session_state.reco_num][
                            "title"
                        ]],
                        "artist": [top_10_with_names.iloc[st.session_state.reco_num][
                            "artist_name"
                        ]],
                        "preference": [-1],
                    }
                ),
            ]
        )
    else:
        # If the record is found, update it
        preferences.loc[preferences["track_id"] == track_id, "preference"] = -1
    st.session_state.reco_num += 1


if like_btn:
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
                        "title": [top_10_with_names.iloc[st.session_state.reco_num][
                            "title"
                        ]],
                        "artist": [top_10_with_names.iloc[st.session_state.reco_num][
                            "artist_name"
                        ]],
                        "preference": [1],
                    }
                ),
            ]
        )
    else:
        # If the record is found, update it
        preferences.loc[preferences["track_id"] == track_id, "preference"] = 1
    st.session_state.reco_num += 1

preferences.to_csv("preferences.csv", index=False)

def render_listen_and_choose():
    track_id = search_track_id(top_10_with_names, st.session_state.reco_num)
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
