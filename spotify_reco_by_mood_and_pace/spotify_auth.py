import requests

# Spotify API credentials
client_id = "ebae4f3be3d1414f8eff4cc24aa0bb8d"
client_secret = "eb1c71cb347443c89676a5deb4911138"
redirect_uri = "http://localhost:8888/callback/"


# Get access token
def get_access_token():
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    token_response = requests.post(
        token_url,
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token_json = token_response.json()
    access_token = token_json["access_token"]
    return access_token


access_token = get_access_token()

# Write the access token to a file
with open("spotify_reco_by_mood_and_pace/access_token.txt", "w") as file:
    file.write(access_token)

print("Access token saved to access_token.txt")
