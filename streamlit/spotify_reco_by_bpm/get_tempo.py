import requests

with open("spotify_reco/models/access_token.txt") as file:
    access_token = file.read()

url = "https://api.spotify.com/v1/audio-features"
params = {"ids": "5Nf86zHHEyU8HYqsxR5SK9,6wP0zUocK5kGLaBYhLbzt5,0n4bITAu0Y0nigrz3MFJMb"}
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(url, params, headers=headers)
print(response.json())
