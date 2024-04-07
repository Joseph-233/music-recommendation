import pytest
import pandas as pd
from spotify_reco.models.predict_features_by_tempo import (
    aggregate_play_count,
    get_predicted_features_name,
    train_lgb,
    predict_features,
    save_model,
    load_model,
)

# Test aggregate_play_count function
def test_aggregate_play_count(tmp_path):
    # Create a temporary CSV file
    csv_file = tmp_path / "test_data.csv"
    # Sample data for testing
    data = {
        "tempo": [120, 140, 160],
        "danceability": [0.5, 0.6, 0.7],
        "valence": [0.3, 0.4, 0.5],
        "play_count": [100, 200, 300],
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)

    # Call the function with the temporary file
    aggregate_play_count(route=csv_file)

    # Read the aggregated data
    aggregated_data = pd.read_csv("spotify_reco/datasets/aggregated_play_count.csv")

    # Check if the aggregated data has correct columns
    assert "tempo" in aggregated_data.columns
    assert "danceability" in aggregated_data.columns
    assert "valence" in aggregated_data.columns
    assert "play_count" in aggregated_data.columns

    # Check if aggregation is correct
    assert len(aggregated_data) == 1
    assert aggregated_data.loc[0, "play_count"] == sum(data["play_count"])


# Assuming the rest of the functions are similar, you can write tests for them as well


# Test get_predicted_features_name function
def test_get_predicted_features_name():
    # Assuming you know the expected output of this function
    expected_features = ["danceability", "valence"]
    assert get_predicted_features_name() == expected_features


# Test train_lgb function
# Note: Since this function relies on external data and involves training a model,
# you may need to mock certain functionalities or split the function into smaller parts for better testing.


# Test predict_features function
def test_predict_features():
    # Assuming you know the expected output for a given input
    tempo = 120  # Example tempo value
    expected_features = {
        "target_danceability": 0.6,
        "target_valence": 0.4,
        "target_key": 5,
        "target_mode": 1,
    }
    assert predict_features(tempo) == expected_features


# Test save_model and load_model functions
def test_save_and_load_model(tmp_path):
    # Assuming you have a trained model object
    model = "dummy_model"

    # Save the model
    model_path = tmp_path / "test_model.joblib"
    save_model(model, model_path)

    # Load the model
    loaded_model = load_model(model_path)

    # Check if the loaded model is the same as the original model
    assert loaded_model == model
