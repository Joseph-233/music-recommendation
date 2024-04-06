import pandas as pd

def read_access_token(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()

def aggregate_user_profile(audio_features_df):
    relevant_features = [
        "danceability", "energy", "valence", "tempo",
        "acousticness", "instrumentalness", "speechiness", "liveness"
    ]
    return audio_features_df[relevant_features].mean().to_dict()