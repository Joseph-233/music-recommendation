import requests
client_id = "ebae4f3be3d1414f8eff4cc24aa0bb8d"
client_secret = "eb1c71cb347443c89676a5deb4911138"

def get_access_token():
    """
    Fetches an access token from the Spotify API.
    """
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(token_url, data=token_data)
    if response.ok:
        return response.json()["access_token"]
    else:
        return "Error: Failed to retrieve access token."

if __name__ == "__main__":
    access_token = get_access_token()
    print(access_token)
