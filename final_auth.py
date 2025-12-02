import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import webbrowser

CLIENT_ID = "8de28aabc43a4643ad29894586a45f68"
CLIENT_SECRET = "34730f008beb4ba29efb4e48a3354c5f"
REDIRECT_URI = "http://127.0.0.1:8080/callback"

print("🔧 Manual Spotify Authentication")
print("=================================")

# Create the authorization URL manually
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state",
    open_browser=False  # We'll open manually
)

# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()
print(f"📋 STEP 1: Copy this URL and paste in your browser:")
print("=" * 50)
print(auth_url)
print("=" * 50)

print("\n📋 STEP 2: After allowing, copy the FULL URL from browser address bar")
print("📋 STEP 3: Paste it here and press Enter")

# Get the callback URL from user
callback_url = input("Paste the callback URL here: ")

# Extract the code from callback URL
if "code=" in callback_url:
    code = sp_oauth.parse_response_code(callback_url)
    print(f"✅ Got authorization code: {code[:10]}...")
    
    # Exchange code for token
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    
    # Save token
    with open("spotify_token.json", "w") as f:
        json.dump(token_info, f, indent=2)
    
    print("✅ SUCCESS! spotify_token.json created!")
    print("🎵 You can now run your gesture control!")
    
else:
    print("❌ Invalid callback URL. Please try again.")