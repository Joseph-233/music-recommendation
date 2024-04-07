import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import webbrowser
import urllib
import os

# Spotify API credentials are sourced from environment variables
client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
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
        self.wfile.write(b"Authentication successful. You can close this tab and return to the application.")

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

# Function to run the server and get the authorization code, not needed in the script directly
# but kept here for completeness. It can be used in an if __name__ == "__main__": block
def run_server_and_get_code():
    # Running the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Open the authorization URL in a browser
    webbrowser.open(auth_full_url)

    # Wait for the authorization code
    global auth_code_received
    auth_code_received = False
    global authorization_code
    authorization_code = ""
    while not auth_code_received:
        pass

    # Shutdown HTTP server after getting the code
    return authorization_code

# Placeholder for where you would get your authorization code in a real-world scenario
# In testing, you can mock this out or provide a code directly to get_access_token
authorization_code = run_server_and_get_code()

# Get the access token
access_token = get_access_token(authorization_code)

# Path to save the access token
access_token_file = "streamlit/spotify_credential/access_token.txt"

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
