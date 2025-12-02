import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

CLIENT_ID = "8de28aabc43a4643ad29894586a45f68"
CLIENT_SECRET = "34730f008beb4ba29efb4e48a3354c5f"
REDIRECT_URI = "http://127.0.0.1:8080"

print("🎵 Starting Spotify Authentication...")

try:
    # Create Spotify OAuth
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state",
        open_browser=True
    )
    
    print("📋 Opening browser for login...")
    
    # Get token - this will open browser and handle everything
    token_info = sp_oauth.get_access_token(as_dict=True)
    
    if token_info:
        # Save token to file
        with open("spotify_token.json", "w") as f:
            json.dump(token_info, f, indent=2)
        
        print("✅ SUCCESS! Token saved to spotify_token.json")
        print("🎵 You can now control Spotify with gestures!")
        
        # Test the token
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user = sp.current_user()
        print(f"👤 Logged in as: {user['display_name']}")
        
    else:
        print("❌ Failed to get token")
        
except Exception as e:
    print(f"❌ Error: {e}")