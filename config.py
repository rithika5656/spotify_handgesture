"""
CONFIGURATION FILE
Centralized configuration for the gesture control system
"""

# ==================== CAMERA SETTINGS ====================
CAMERA_CONFIG = {
    'camera_id': 0,              # Webcam device ID (usually 0)
    'width': 640,                # Video frame width
    'height': 480,               # Video frame height
    'fps': 30,                   # Target frames per second
}

# ==================== HAND DETECTION SETTINGS ====================
HAND_DETECTION_CONFIG = {
    'mode': False,               # Static image mode (False for video)
    'max_hands': 1,              # Maximum hands to detect
    'detection_confidence': 0.5, # Min confidence for detection
    'tracking_confidence': 0.5,  # Min confidence for tracking
}

# ==================== GESTURE CLASSIFICATION SETTINGS ====================
GESTURE_CONFIG = {
    'model_type': 'random_forest',  # 'svm', 'random_forest', 'neural_network'
    'confidence_threshold': 0.6,    # Min confidence to trigger action
    'gesture_history_size': 5,      # Smoothing history size
}

# ==================== MODEL SETTINGS ====================
MODEL_CONFIG = {
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42,
    },
    'svm': {
        'kernel': 'rbf',
        'C': 1.0,
        'gamma': 'scale',
    },
    'neural_network': {
        'hidden_layer_sizes': (128, 64, 32),
        'max_iter': 1000,
        'random_state': 42,
    }
}

# ==================== ACTION SETTINGS ====================
ACTION_CONFIG = {
    'cooldown_period': 0.3,      # Cooldown between actions (seconds)
    'volume_step': 0.05,         # Volume change per gesture (5%)
    'enable_animations': True,   # Show animations on screen
}

# ==================== FEATURE EXTRACTION SETTINGS ====================
FEATURE_CONFIG = {
    'extract_distances': True,   # Extract distance features
    'extract_angles': True,      # Extract angle features
    'normalize_features': True,  # Normalize feature values
}

# ==================== TRAINING SETTINGS ====================
TRAINING_CONFIG = {
    'test_split': 0.2,           # 20% for testing, 80% for training
    'random_state': 42,          # Random seed
    'samples_per_gesture': 50,   # Samples to collect per gesture
}

# ==================== GESTURE MAPPING ====================
GESTURE_MAPPING = {
    0: "volume_up",              # PALM
    1: "volume_down",            # FIST
    2: "play_pause",             # PINCH
    3: "next_track",             # POINT
    4: "previous_track",         # V_SIGN
}

# ==================== DISPLAY SETTINGS ====================
DISPLAY_CONFIG = {
    'show_landmarks': True,      # Show hand landmarks
    'show_fps': True,            # Show FPS counter
    'show_confidence': True,     # Show confidence score
    'show_volume': True,         # Show volume indicator
    'show_gesture_name': True,   # Show detected gesture name
}

# ==================== LOGGING SETTINGS ====================
LOG_CONFIG = {
    'enable_logging': True,
    'log_level': 'INFO',         # 'DEBUG', 'INFO', 'WARNING', 'ERROR'
    'log_file': 'gesture_control.log',
}

# ==================== DATA PATHS ====================
DATA_PATHS = {
    'data_dir': 'data',
    'models_dir': 'data',
    'logs_dir': 'logs',
    'model_name': 'gesture_model_random_forest',
}

# ==================== GESTURE NAMES ====================
GESTURE_NAMES = {
    0: "PALM",
    1: "FIST",
    2: "PINCH",
    3: "POINT",
    4: "V_SIGN",
}

# ==================== ACTION DESCRIPTIONS ====================
ACTION_DESCRIPTIONS = {
    'volume_up': '📈 Volume Up',
    'volume_down': '📉 Volume Down',
    'play_pause': '▶️ Play/Pause',
    'next_track': '⏭️ Next Track',
    'previous_track': '⏮️ Previous Track',
}

def get_config():
    """Get complete configuration dictionary"""
    return {
        'camera': CAMERA_CONFIG,
        'hand_detection': HAND_DETECTION_CONFIG,
        'gesture': GESTURE_CONFIG,
        'model': MODEL_CONFIG,
        'action': ACTION_CONFIG,
        'feature': FEATURE_CONFIG,
        'training': TRAINING_CONFIG,
        'mapping': GESTURE_MAPPING,
        'display': DISPLAY_CONFIG,
        'logging': LOG_CONFIG,
        'paths': DATA_PATHS,
    }

def print_config():
    """Print all configuration settings"""
    import json
    config = get_config()
    print("\n" + "="*60)
    print("SYSTEM CONFIGURATION")
    print("="*60 + "\n")
    print(json.dumps(config, indent=2))
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print_config()
