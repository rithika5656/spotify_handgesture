"""
MODULE 5: Media Control
Control system volume and media playback using pycaw and pyautogui
"""

import pyautogui
import time
from ctypes import *
from comtypes import CLSCTX_ALL
from pycaw.pycaw import IAudioEndpointVolume, IMMDevice, IMMDeviceEnumerator
from pycaw.constants import CLSCTX_ALL

class MediaController:
    """
    Control system volume and media playback
    Uses pycaw for volume and pyautogui for media keys
    """
    
    # Media key press duration (seconds)
    KEY_PRESS_DURATION = 0.1
    
    def __init__(self):
        """Initialize media controller"""
        self.volume_control = None
        self.current_volume = 0
        self.last_action_time = 0
        self.action_cooldown = 0.3  # Cooldown between actions (seconds)
        
        self._init_volume_control()
    
    def _init_volume_control(self):
        """Initialize Windows audio volume control"""
        try:
            devices = POINTER(IMMDevice)()
            hr = cast(devices, POINTER(POINTER(IMMDevice)))
            
            # Get device enumerator
            from comtypes.client import CreateObject
            device_enumerator = CreateObject(
                "{BCDE0395-E52F-467C-8E3D-C4579291692E}",
                interface=IMMDeviceEnumerator,
                clsctx=CLSCTX_ALL
            )
            
            # Get default audio device
            device = device_enumerator.GetDefaultAudioEndpoint(0, 1)
            
            # Get volume control
            self.volume_control = cast(
                device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None),
                POINTER(IAudioEndpointVolume)
            )
            
            print("✓ Volume control initialized successfully")
        except Exception as e:
            print(f"⚠ Error initializing volume control: {e}")
            print("Volume control may not work on this system")
    
    def get_volume(self):
        """
        Get current system volume (0.0 - 1.0)
        
        Returns:
            Volume level (0.0 to 1.0)
        """
        try:
            if self.volume_control:
                return self.volume_control.GetMasterVolumeLevelScalar()
            return 0.0
        except Exception as e:
            print(f"Error getting volume: {e}")
            return 0.0
    
    def set_volume(self, volume):
        """
        Set system volume
        
        Args:
            volume: Volume level (0.0 - 1.0)
        """
        try:
            if self.volume_control:
                # Ensure volume is in valid range
                volume = max(0.0, min(1.0, volume))
                self.volume_control.SetMasterVolumeLevelScalar(volume, None)
                self.current_volume = volume
        except Exception as e:
            print(f"Error setting volume: {e}")
    
    def increase_volume(self, step=0.05):
        """
        Increase volume by step
        
        Args:
            step: Volume increase step (default 0.05 = 5%)
        """
        if self._check_cooldown():
            current = self.get_volume()
            self.set_volume(current + step)
            self.last_action_time = time.time()
    
    def decrease_volume(self, step=0.05):
        """
        Decrease volume by step
        
        Args:
            step: Volume decrease step (default 0.05 = 5%)
        """
        if self._check_cooldown():
            current = self.get_volume()
            self.set_volume(current - step)
            self.last_action_time = time.time()
    
    def play_pause(self):
        """Toggle play/pause"""
        if self._check_cooldown():
            pyautogui.press('playpause')
            self.last_action_time = time.time()
    
    def next_track(self):
        """Skip to next track"""
        if self._check_cooldown():
            pyautogui.press('nexttrack')
            self.last_action_time = time.time()
    
    def previous_track(self):
        """Go to previous track"""
        if self._check_cooldown():
            pyautogui.press('prevtrack')
            self.last_action_time = time.time()
    
    def mute(self):
        """Mute audio"""
        if self._check_cooldown():
            pyautogui.press('volumemute')
            self.last_action_time = time.time()
    
    def unmute(self):
        """Unmute audio"""
        if self._check_cooldown():
            pyautogui.press('volumemute')
            self.last_action_time = time.time()
    
    def _check_cooldown(self):
        """
        Check if enough time has passed since last action
        Prevents gesture from triggering too many times
        
        Returns:
            True if action should be executed
        """
        current_time = time.time()
        return (current_time - self.last_action_time) >= self.action_cooldown
    
    def execute_action(self, action):
        """
        Execute media control action
        
        Args:
            action: Action string (from ActionMapper)
        """
        from modules.action_mapper import ActionMapper
        
        if action == ActionMapper.VOLUME_UP:
            self.increase_volume()
        elif action == ActionMapper.VOLUME_DOWN:
            self.decrease_volume()
        elif action == ActionMapper.PLAY_PAUSE:
            self.play_pause()
        elif action == ActionMapper.NEXT_TRACK:
            self.next_track()
        elif action == ActionMapper.PREVIOUS_TRACK:
            self.previous_track()
        elif action == ActionMapper.MUTE:
            self.mute()
        elif action == ActionMapper.UNMUTE:
            self.unmute()
