# Modifying the script to write the access token to a file
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import webbrowser
import urllib
import os

# Spotify API credentials
with open("./spotify_reco/models/client_id.txt", "r") as file:
    client_id = file.read().strip()  #'ebae4f3be3d1414f8eff4cc24aa0bb8d'
with open("./spotify_reco/models/client_secret.txt", "r") as file:
    client_secret = file.read().strip()  #'eb1c71cb347443c89676a5deb4911138'
redirect_uri = "http://localhost:8888/callback/"

# Scope for user data access
scope = "user-top-read"

# Generate the authorization URL
auth_url = "https://accounts.spotify.com/authorize"
auth_params = {
    "response_type": "code",
    "client_id": client_id,
    "scope": scope,
    "redirect_uri": redirect_uri,
}
auth_query = urllib.parse.urlencode(auth_params)
auth_full_url = f"{auth_url}?{auth_query}"


# HTTP Server to handle OAuth callback
class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            b"Authentication successful. You can close this tab and return to the notebook."
        )

        # Extract the authorization code
        url_path = self.path
        url_query = urllib.parse.urlparse(url_path).query
        params = urllib.parse.parse_qs(url_query)
        auth_code = params["code"][0]

        # Signal that we have received the code
        global auth_code_received
        auth_code_received = True
        global authorization_code
        authorization_code = auth_code


# Start the server
def start_server():
    server_address = ("", 8888)
    httpd = HTTPServer(server_address, OAuthCallbackHandler)
    httpd.serve_forever()


# Get access token
def get_access_token(auth_code):
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    access_token = token_json["access_token"]
    return access_token


# Running the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Open the authorization URL in a browser
webbrowser.open(auth_full_url)

# Wait for the authorization code
auth_code_received = False
authorization_code = ""
while not auth_code_received:
    pass

# Get the access token
access_token = get_access_token(authorization_code)

access_token_file = "./spotify_reco/models/access_token.txt"

# Check if the directory exists, if not, create it
if not os.path.exists(os.path.dirname(access_token_file)):
    os.makedirs(os.path.dirname(access_token_file))

# Write the access token to a file
try:
    with open(access_token_file, "w") as f:
        f.write(access_token)
    print(f"Access token saved to {access_token_file}")
except Exception as e:
    print(f"Error writing to file: {e}")
