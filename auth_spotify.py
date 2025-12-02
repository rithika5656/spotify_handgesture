import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "8de28aabc43a4643ad29894586a45f68"
CLIENT_SECRET = "34730f008beb4ba29efb4e48a3354c5f"
REDIRECT_URI = "http://127.0.0.1:8080/callback"

SCOPE = "user-modify-playback-state user-read-playback-state"

def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path="spotify_token.json",   # token file will be created
        open_browser=True
    ))

    print("Login complete! Token saved as spotify_token.json")

if __name__ == "__main__":
    main()
