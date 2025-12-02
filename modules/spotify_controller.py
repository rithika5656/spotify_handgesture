"""
SPOTIFY INTEGRATION MODULE
Control Spotify specifically using hand gestures
"""

import pyautogui
import time
import subprocess
import psutil

class SpotifyController:
    """
    Control Spotify app using hand gestures
    Detects if Spotify is running and focuses the window
    """
    
    def __init__(self):
        """Initialize Spotify controller"""
        self.spotify_process = None
        self.last_action_time = 0
        self.action_cooldown = 0.5  # Cooldown between actions
        self.is_spotify_open = False
        
        print("🎵 Spotify Controller initialized")
    
    def is_spotify_running(self):
        """
        Check if Spotify process is running
        
        Returns:
            True if Spotify is running, False otherwise
        """
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if 'spotify' in proc.info['name'].lower():
                    self.spotify_process = proc
                    self.is_spotify_open = True
                    return True
            self.is_spotify_open = False
            return False
        except Exception as e:
            print(f"Error checking Spotify: {e}")
            return False
    
    def launch_spotify(self):
        """
        Launch Spotify application
        
        Returns:
            True if successful, False otherwise
        """
        try:
            print("🚀 Launching Spotify...")
            
            # Try to launch Spotify from default location
            spotify_path = r"C:\Users\rithi\AppData\Roaming\Spotify\spotify.exe"
            
            try:
                subprocess.Popen(spotify_path)
                time.sleep(3)  # Wait for Spotify to launch
                print("✓ Spotify launched successfully")
                return True
            except FileNotFoundError:
                print("⚠️  Spotify not found at default location")
                print("Trying alternative launch method...")
                
                # Alternative: use Windows search
                os.startfile("spotify.exe")
                time.sleep(3)
                print("✓ Spotify launched")
                return True
                
        except Exception as e:
            print(f"✗ Error launching Spotify: {e}")
            return False
    
    def focus_spotify_window(self):
        """
        Focus on Spotify window
        Uses Windows API to bring Spotify to foreground
        """
        try:
            import win32gui
            import win32con
            
            # Find Spotify window
            hwnd = win32gui.FindWindow(None, "Spotify")
            
            if hwnd:
                # Bring window to foreground
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.3)
                return True
            else:
                print("⚠️  Spotify window not found")
                return False
                
        except ImportError:
            print("⚠️  pywin32 not installed. Install with: pip install pywin32")
            return False
        except Exception as e:
            print(f"Error focusing Spotify: {e}")
            return False
    
    def _check_cooldown(self):
        """Check if enough time has passed since last action"""
        current_time = time.time()
        return (current_time - self.last_action_time) >= self.action_cooldown
    
    def play_pause(self):
        """Play/Pause Spotify"""
        if self._check_cooldown():
            try:
                # Spotify responds to spacebar
                pyautogui.press('space')
                self.last_action_time = time.time()
                print("▶️ Play/Pause triggered")
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
    
    def next_track(self):
        """Skip to next track in Spotify"""
        if self._check_cooldown():
            try:
                # Ctrl+Right arrow for next track
                pyautogui.hotkey('ctrl', 'right')
                self.last_action_time = time.time()
                print("⏭️ Next track triggered")
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
    
    def previous_track(self):
        """Go to previous track in Spotify"""
        if self._check_cooldown():
            try:
                # Ctrl+Left arrow for previous track
                pyautogui.hotkey('ctrl', 'left')
                self.last_action_time = time.time()
                print("⏮️ Previous track triggered")
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
    
    def volume_up(self, step=0.05):
        """Increase Spotify volume"""
        if self._check_cooldown():
            try:
                # Use Windows volume control via media keys
                pyautogui.press('volumeup')
                self.last_action_time = time.time()
                print("📈 Volume up triggered")
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
    
    def volume_down(self, step=0.05):
        """Decrease Spotify volume"""
        if self._check_cooldown():
            try:
                # Use Windows volume control via media keys
                pyautogui.press('volumedown')
                self.last_action_time = time.time()
                print("📉 Volume down triggered")
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
    
    def like_track(self):
        """Like/Heart current track (adds to liked songs)"""
        if self._check_cooldown():
            try:
                # Ctrl+L to like track in Spotify
                pyautogui.hotkey('ctrl', 'l')
                self.last_action_time = time.time()
                print("❤️ Track liked")
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
    
    def open_queue(self):
        """Open queue in Spotify"""
        if self._check_cooldown():
            try:
                # Ctrl+Q opens queue
                pyautogui.hotkey('ctrl', 'q')
                self.last_action_time = time.time()
                print("📋 Queue opened")
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
    
    def execute_action(self, action):
        """
        Execute Spotify action
        
        Args:
            action: Action string (from ActionMapper)
        """
        if not self.is_spotify_running():
            print("⚠️  Spotify is not running!")
            print("Launch Spotify first: self.launch_spotify()")
            return False
        
        # Ensure Spotify window is focused
        self.focus_spotify_window()
        
        actions = {
            'volume_up': self.volume_up,
            'volume_down': self.volume_down,
            'play_pause': self.play_pause,
            'next_track': self.next_track,
            'previous_track': self.previous_track,
            'like_track': self.like_track,
            'open_queue': self.open_queue,
        }
        
        action_func = actions.get(action)
        if action_func:
            return action_func()
        else:
            print(f"Unknown action: {action}")
            return False
    
    def get_status(self):
        """Get Spotify status"""
        status = {
            'is_running': self.is_spotify_running(),
            'process_id': self.spotify_process.pid if self.spotify_process else None,
            'cooldown_active': not self._check_cooldown(),
        }
        return status
