import pytest
from spotify_reco_by_mood_and_pace.main import get_access_token  
import time

def test_get_access_token():
    access_token = get_access_token()
    assert isinstance(access_token, str) and len(access_token) > 0, "Access token should be a non-empty string"



class CountPresses:
    def __init__(self):
        self.count = 0
        self.start_time = time.time()
        self.ppm = 0

    def count_spacebar_presses(self, e):
        if e.get('event_type') == "up":  # Simulate checking for the key release.
            self.count += 1
            time_passed = time.time() - self.start_time
            self.ppm = self.count * 60 / time_passed  # Pace per minute

def simulate_spacebar_press(counter):
    # Simulate the key release event.
    event = {'event_type': 'up'}
    counter.count_spacebar_presses(event)

def test_integration():
    counter = CountPresses()
    presses = 10
    
    # Simulate 10 spacebar presses.
    for _ in range(presses):
        simulate_spacebar_press(counter)
        time.sleep(0.1)  # Simulate a short delay between presses.

    # Assertions to verify the behavior.
    assert counter.count == presses, f"Expected {presses} presses, got {counter.count}"
    
    # Because we're simulating time, we can't precisely assert ppm without knowing exact timings,
    # but we can check if it's in the expected range.
    expected_ppm = presses * 60 / (0.1 * presses)  # Simplified calculation based on sleep time.
    assert round(counter.ppm) == round(expected_ppm), f"Expected PPM around {expected_ppm}, got {counter.ppm}"

    print("Integration test passed.")

if __name__ == "__main__":
    test_integration()
