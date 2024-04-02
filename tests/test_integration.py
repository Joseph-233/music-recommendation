import pytest
from spotify_reco_by_mood_and_pace.main import get_access_token  
from your_recommendation_engine_module import get_song_recommendations


def test_get_access_token():
    access_token = get_access_token()
    assert isinstance(access_token, str) and len(access_token) > 0, "Access token should be a non-empty string"


# Sample data for testing
test_data = [
    (60, "classical", 5),  # Lower heartbeat, classical taste, expecting 5 recommendations
    (120, "workout", 5),  # Higher heartbeat, workout taste, expecting 5 recommendations
    (80, "pop", 5),  # Moderate heartbeat, pop taste, expecting 5 recommendations
]

@pytest.mark.parametrize("heartbeat,taste,expected_count", test_data)
def test_get_song_recommendations(heartbeat, taste, expected_count):
    # Call the recommendation engine function
    recommendations = get_song_recommendations(heartbeat, taste)
    
    # Check if the returned recommendations match the expected format and count
    assert isinstance(recommendations, list), "Recommendations should be returned as a list"
    assert len(recommendations) == expected_count, f"Expected {expected_count} recommendations, got {len(recommendations)}"
    for song in recommendations:
        assert isinstance(song, dict), "Each recommendation should be a dictionary"
        assert "title" in song and "artist" in song, "Each recommendation should include title and artist"

