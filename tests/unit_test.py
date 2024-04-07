import unittest
import os
from spotify_reco.models.predict_features_by_tempo import aggregate_play_count, get_predicted_features_name, predict_features

class TestSpotifyRecoSimple(unittest.TestCase):

    def setUp(self):
        # Setup any required variables or perform preliminary steps
        self.track_data_route = "spotify_reco/datasets/dataset_ready.csv"
        self.aggregated_play_count_route = "spotify_reco/datasets/aggregated_play_count.csv"

    def test_aggregate_play_count(self):
        # Call the function to test
        aggregate_play_count(self.track_data_route)
        # Verify the file was created and is not empty
        self.assertTrue(os.path.exists(self.aggregated_play_count_route), "Aggregated play count file should exist")
        self.assertGreater(os.path.getsize(self.aggregated_play_count_route), 0, "File should not be empty")

    def test_get_predicted_features_name(self):
        # Expected feature names based on your dataset columns
        expected_feature_names = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
        feature_names = get_predicted_features_name()
        # Check if the returned list matches the expected feature names
        self.assertListEqual(feature_names, expected_feature_names, "The feature names should match the expected list")


    @classmethod
    def tearDownClass(cls):
        # Clean up any files or resources if necessary
        # Example: os.remove("path_to_file")

        pass

if __name__ == '__main__':
    unittest.main()
