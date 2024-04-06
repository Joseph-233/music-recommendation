import os
import requests

# Constants
REDIRECT_URI = "http://localhost:8888/callback/"
TOKEN_URL = "https://accounts.spotify.com/api/token"

def get_access_token(client_id, client_secret):
    """
    Fetches an access token from the Spotify API.
    """
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(
        TOKEN_URL,
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()  # This will raise an error if the request fails
    token_json = response.json()
    return token_json["access_token"]

def main():
    """
    Main function to get the Spotify access token and save it to a file.
    """
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError("Spotify credentials are not set in the environment.")

    access_token = get_access_token(client_id, client_secret)

    # Write the access token to a file
    with open("spotify_reco_by_mood_and_pace/access_token.txt", "w") as file:
        file.write(access_token)

    print("Access token saved to access_token.txt")

if __name__ == "__main__":
    main()
