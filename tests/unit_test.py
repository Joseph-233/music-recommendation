import pytest
from spotify_reco.models.predict_features_by_tempo import predict_features

# Mocking the global model object
class MockModel:
    def predict(self, input):
        return [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]]

@pytest.fixture
def mock_model(monkeypatch):
    monkeypatch.setattr('spotify_reco.models.predict_features_by_tempo.model', MockModel())

def test_predict_features(mock_model):
    tempo = 120
    expected_output = {
        "target_danceability": 0.1,
        "target_energy": 0.2,
        "target_key": 0.3,
        "target_loudness": 0.4,
        "target_mode": 0.5,
        "target_speechiness": 0.6,
        "target_valence": 0.7,
    }
    assert predict_features(tempo) == expected_output
