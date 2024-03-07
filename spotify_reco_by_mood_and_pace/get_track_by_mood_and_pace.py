# uncomment "import spotify_auth" at first time and every 1 hour
#import spotify_auth

import count_presses
import requests
import time, traceback
import keyboard


access_token = ""
with open("spotify_reco_by_mood_and_pace/access_token.txt") as file:
    access_token = file.read()


# Make a GET request to the Spotify API
# 19tf1og71pOYoYOdqyozs2 sarah chen
# 4QQgXkCYTt3BlENzhyNETg earth wind and fire
# 6eUKZXaKkcviH0Ku9w2n3V edsheeran
def get_tracks_by_mood_and_pace(ppm):
    try:

        url = "https://api.spotify.com/v1/recommendations"
        params = {
            "limit": 3,
            "seed_artists": "6eUKZXaKkcviH0Ku9w2n3V",
            "target_tempo": ppm,
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, params, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            tracks = response.json()["tracks"]
            tracks_name_url = []
            for track in tracks:
                tracks_name_url.append(
                    (track["name"], track["external_urls"]["spotify"])
                )
            print(tracks_name_url)
            return tracks_name_url
        else:
            print("Error:", response.status_code)
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()


counter = count_presses.CountPresses()
keyboard.hook_key("space", counter.count_spacebar_presses)
while True:
    time.sleep(10)
    get_tracks_by_mood_and_pace(counter.ppm)
