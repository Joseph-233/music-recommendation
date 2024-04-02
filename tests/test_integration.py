import pytest
from spotify_reco_by_mood_and_pace.main import get_access_token  
import time
import keyboard

def test_get_access_token():
    access_token = get_access_token()
    assert isinstance(access_token, str) and len(access_token) > 0, "Access token should be a non-empty string"




class CountPresses:
    def __init__(self):
        self.count = 0
        self.start_time = time.time()
        self.ppm = 0

    def count_spacebar_presses(self, e):
        if e.event_type == "up":  # This condition checks if the key is released.
            self.count += 1
            print(f"Spacebar pressed {self.count} times")
            time_passed = time.time() - self.start_time
            print(f"Time passed: {time_passed} seconds")
            self.ppm = self.count * 60 / time_passed  # Pace per minute
            print(f"Pace per minute: {self.ppm}")

def main():
    counter = CountPresses()
    print("Start pressing the spacebar. Press ESC to stop.")
    
    # Hook to the spacebar key up event.
    keyboard.on_release_key("space", counter.count_spacebar_presses)
    
    # Wait for the ESC key to stop the program.
    keyboard.wait('esc')
    
    # Optionally, you can print out the final counts, time, and ppm when ESC is pressed.
    print(f"Final count: {counter.count}")
    final_time_passed = time.time() - counter.start_time
    print(f"Total time passed: {final_time_passed} seconds")
    final_ppm = counter.count * 60 / final_time_passed
    print(f"Final pace per minute: {final_ppm}")

if __name__ == "__main__":
    main()


