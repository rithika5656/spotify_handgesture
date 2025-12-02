"""
Spotify Web API helper using spotipy

Usage:
- Create a Spotify Developer App and set Redirect URI to: http://localhost:8888/callback
- Set CLIENT_ID and CLIENT_SECRET as env vars or pass them to SpotifyAPI
- Run `python auth_spotify.py` once to perform OAuth and save tokens to `spotify_token.json`
- In your `spotify_controller.py`, instantiate SpotifyAPI and call `play_pause()`, `next_track()`, etc.
"""

import os
import json
import logging
from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth

_log = logging.getLogger(__name__)

DEFAULT_SCOPE = "user-modify-playback-state user-read-playback-state user-read-currently-playing user-read-private user-library-modify"
TOKEN_FILE = "spotify_token.json"

class SpotifyAPI:
    def __init__(self, client_id: Optional[str]=None, client_secret: Optional[str]=None, redirect_uri: str="http://localhost:8888/callback", scope: str=DEFAULT_SCOPE):
        self.client_id = client_id or os.environ.get("SPOTIFY_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.sp: Optional[spotipy.Spotify] = None
        self.oauth: Optional[SpotifyOAuth] = None

        if not self.client_id or not self.client_secret:
            _log.debug("Spotify client credentials not provided; please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET env vars or pass them to SpotifyAPI.")

    def _get_oauth(self) -> SpotifyOAuth:
        if self.oauth is None:
            self.oauth = SpotifyOAuth(client_id=self.client_id,
                                      client_secret=self.client_secret,
                                      redirect_uri=self.redirect_uri,
                                      scope=self.scope,
                                      cache_path=TOKEN_FILE)
        return self.oauth

    def authorize(self):
        """Run the OAuth flow (opens browser) and saves token to `spotify_token.json`."""
        oauth = self._get_oauth()
        token_info = oauth.get_access_token(as_dict=True)
        if not token_info:
            raise RuntimeError("Failed to obtain token; ensure client_id/client_secret and redirect_uri are correct.")

        with open(TOKEN_FILE, "w") as f:
            json.dump(token_info, f)
        _log.info("Saved token to %s", TOKEN_FILE)
        self.sp = spotipy.Spotify(auth=token_info["access_token"]) 
        return token_info

    def load_token(self):
        oauth = self._get_oauth()
        token_info = None
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                token_info = json.load(f)

        if token_info and oauth.is_token_expired(token_info):
            token_info = oauth.refresh_access_token(token_info.get("refresh_token"))
            with open(TOKEN_FILE, "w") as f:
                json.dump(token_info, f)

        if token_info:
            self.sp = spotipy.Spotify(auth=token_info.get("access_token"))
            return True
        return False

    def get_spotify(self) -> Optional[spotipy.Spotify]:
        if self.sp is None:
            ok = self.load_token()
            if not ok:
                _log.warning("No valid token found. Call authorize() to perform OAuth.")
                return None
        return self.sp

    # Playback controls
    def play_pause(self):
        sp = self.get_spotify()
        if not sp:
            return False
        current = sp.current_playback()
        if not current or not current.get("is_playing"):
            sp.start_playback()
            return True
        else:
            sp.pause_playback()
            return True

    def next_track(self):
        sp = self.get_spotify()
        if not sp:
            return False
        sp.next_track()
        return True

    def previous_track(self):
        sp = self.get_spotify()
        if not sp:
            return False
        sp.previous_track()
        return True

    def set_volume_percent(self, percent: int):
        sp = self.get_spotify()
        if not sp:
            return False
        percent = max(0, min(100, int(percent)))
        sp.volume(percent)
        return True

    def get_current_playback(self):
        sp = self.get_spotify()
        if not sp:
            return None
        return sp.current_playback()
