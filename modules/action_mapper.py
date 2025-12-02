"""
MODULE 4: Action Mapping
Map classified gestures to media control actions
Easy to modify and extend for different use cases
"""

class ActionMapper:
    """
    Map gesture classes to media control actions
    Can be easily customized for different applications
    """
    
    # Action types
    VOLUME_UP = "volume_up"
    VOLUME_DOWN = "volume_down"
    PLAY_PAUSE = "play_pause"
    NEXT_TRACK = "next_track"
    PREVIOUS_TRACK = "previous_track"
    MUTE = "mute"
    UNMUTE = "unmute"
    
    # Default gesture-to-action mapping
    DEFAULT_MAPPING = {
        0: VOLUME_UP,          # PALM
        1: VOLUME_DOWN,        # FIST
        2: PLAY_PAUSE,         # PINCH
        3: NEXT_TRACK,         # POINT (right)
        4: PREVIOUS_TRACK,     # V_SIGN (left)
    }
    
    def __init__(self, custom_mapping=None):
        """
        Initialize action mapper
        
        Args:
            custom_mapping: Dict of {gesture_class: action}
        """
        self.mapping = custom_mapping if custom_mapping else self.DEFAULT_MAPPING.copy()
        self.last_action = None
        self.action_counter = 0
    
    def get_action(self, gesture_class):
        """
        Get action for given gesture class
        
        Args:
            gesture_class: Gesture class index
            
        Returns:
            Action string
        """
        action = self.mapping.get(gesture_class, None)
        
        if action and action != self.last_action:
            self.last_action = action
            self.action_counter = 0
        
        self.action_counter += 1
        return action
    
    def set_custom_mapping(self, gesture_class, action):
        """
        Set custom mapping for a gesture
        
        Args:
            gesture_class: Gesture class index
            action: Action to map to
        """
        self.mapping[gesture_class] = action
        print(f"Mapped gesture {gesture_class} to {action}")
    
    def reset_mapping(self):
        """Reset to default mapping"""
        self.mapping = self.DEFAULT_MAPPING.copy()
        print("Mapping reset to default")
    
    def get_mapping(self):
        """Get current mapping"""
        return self.mapping.copy()
    
    @staticmethod
    def get_action_description(action):
        """
        Get human-readable description of action
        
        Args:
            action: Action string
            
        Returns:
            Description
        """
        descriptions = {
            ActionMapper.VOLUME_UP: "📈 Volume Up",
            ActionMapper.VOLUME_DOWN: "📉 Volume Down",
            ActionMapper.PLAY_PAUSE: "▶️ Play/Pause",
            ActionMapper.NEXT_TRACK: "⏭️ Next Track",
            ActionMapper.PREVIOUS_TRACK: "⏮️ Previous Track",
            ActionMapper.MUTE: "🔇 Mute",
            ActionMapper.UNMUTE: "🔊 Unmute",
        }
        return descriptions.get(action, "Unknown Action")
