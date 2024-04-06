import time


class CountPresses:
    def __init__(self):
        self.count = 0
        self.start_time = time.time()
        self.ppm = 0

    def count_spacebar_presses(self, e):
        if e.event_type == "up":
            self.count += 1
            print(f"Spacebar pressed {self.count} times")
            time_passed = time.time() - self.start_time
            print(f"Time passed: {time_passed}")
            self.ppm = self.count * 60 / time_passed  # Pace per minute
            print(f"Pace per minute: {self.ppm}")
