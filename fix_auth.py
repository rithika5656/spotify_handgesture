import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# Your exact credentials from dashboard
CLIENT_ID = "8de28aabc43a4643ad29894586a45f68"
CLIENT_SECRET = "34730f008beb4ba29efb4e48a3354c5f"
REDIRECT_URI = "http://127.0.0.1:8080/callback"

print("🔧 Starting Spotify authentication...")
print(f"Client ID: {CLIENT_ID[:10]}...")
print(f"Redirect URI: {REDIRECT_URI}")

try:
    # Create OAuth manager
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET, 
        redirect_uri=REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state",
        open_browser=True
    )
    
    print("🎵 Opening browser for Spotify login...")
    
    # This will open browser and wait for you to login
    token_info = sp_oauth.get_access_token(as_dict=True)
    
    if token_info:
        # Save token to file
        with open("spotify_token.json", "w") as f:
            json.dump(token_info, f, indent=2)
        
        print("✅ SUCCESS! Token saved to spotify_token.json")
        print(f"📁 File created with token data")
        
        # Verify the file exists
        import os
        if os.path.exists("spotify_token.json"):
            print("📄 File verification: spotify_token.json EXISTS!")
        else:
            print("❌ File verification: File NOT created!")
            
    else:
        print("❌ Failed to get token")
        
except Exception as e:
    print(f"❌ Error: {e}")