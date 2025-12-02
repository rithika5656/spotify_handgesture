# 🎵 SPOTIFY GESTURE CONTROL SETUP GUIDE

## 🎯 What This Does

Control Spotify music player with **hand gestures**:
- ✋ PALM → Volume Up
- ✊ FIST → Volume Down  
- 🤏 PINCH → Play/Pause
- 👉 POINT → Next Track
- ✌ V_SIGN → Previous Track

**Uses:** Your webcam + hand gestures + ML model to control Spotify in real-time!

---

## 📋 Prerequisites

✅ Already have main project setup:
- Virtual environment created
- Dependencies installed
- ML model trained

✅ Spotify installed on your computer:
- Download from https://www.spotify.com/download
- Free or Premium account

---

## 🚀 Quick Start (4 steps)

### Step 1: Update Dependencies
```bash
# Activate virtual environment first
cd "c:\Users\rithi\OneDrive\Desktop\HAND GESTURE"
.\venv\Scripts\activate

# Install additional packages for Spotify control
pip install -r requirements.txt
```

### Step 2: Start Spotify
```bash
# Open Spotify app manually and log in
# OR: The script will ask to launch it
```

### Step 3: Run Spotify Gesture Control
```bash
python spotify_gesture_control.py
```

### Step 4: Control Spotify with Gestures!
```
Show your hand in front of the camera
Different gestures will control Spotify in real-time
Press Q to quit
```

---

## 📊 What Happens

```
┌─────────────────────┐
│   Webcam Feed       │
└────────┬────────────┘
         │
    ┌────▼────┐
    │ Hand    │
    │Detection│ (21 landmarks)
    └────┬────┘
         │
    ┌────▼──────────┐
    │Feature Extract│ (8 features)
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │ML Classifier  │ (Gesture detection)
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │Action Mapper  │ (Gesture → action)
    └────┬──────────┘
         │
    ┌────▼──────────────┐
    │Spotify Controller  │ (Send commands)
    └────┬──────────────┘
         │
    ✓ Spotify responds to your gestures!
```

---

## 🎮 How to Use

### During Live Control:

**Keyboard Controls:**
- **Q** - Quit application
- **S** - Toggle settings (reserved for future use)

**Gestures:**
- Show your hand clearly in front of camera
- Make one of the 5 gestures
- Spotify will respond!

**Tips:**
- Keep hand 30-60cm from camera
- Good lighting is important
- Make clear, deliberate gestures
- One gesture at a time

---

## 🔊 Spotify Keyboard Shortcuts

These are the shortcuts the gesture controller uses:

| Gesture | Keyboard Command | Action |
|---------|------------------|--------|
| ✋ PALM | Volume Up Key | Increase system volume |
| ✊ FIST | Volume Down Key | Decrease system volume |
| 🤏 PINCH | SPACE | Play/Pause |
| 👉 POINT | CTRL + Right Arrow | Next Track |
| ✌ V_SIGN | CTRL + Left Arrow | Previous Track |

---

## ⚡ File Structure

```
New files added:
├── spotify_gesture_control.py      Main Spotify-specific app
├── modules/spotify_controller.py   Spotify control module
└── HOW_TO_RUN_SPOTIFY.md          This guide

Updated files:
├── requirements.txt               (Added psutil, pywin32)
```

---

## 🆘 Troubleshooting

### ❌ "Spotify is not running!"
**Solution:**
- Manually open Spotify app
- Wait for it to fully load
- Log in if needed
- Then run the script

### ❌ "Gesture detected but Spotify not responding"
**Solution:**
- Click on Spotify window to focus it
- Make sure Spotify is active (not minimized)
- Try increasing volume manually to verify it works
- Check if keyboard shortcuts work (SPACE = play/pause)

### ❌ "ModuleNotFoundError: psutil"
**Solution:**
```bash
pip install psutil
```

### ❌ "ModuleNotFoundError: pywin32"
**Solution:**
```bash
pip install pywin32
```

### ❌ "Low accuracy on gestures"
**Solution:**
- Collect more training data (100+ per gesture)
- Improve lighting conditions
- Vary your hand orientation
- Retrain model: `python train_model.py`

### ❌ "Camera not working"
**Solution:**
- Check webcam connection
- Restart the application
- Try another USB camera
- Check permissions

### ❌ "Spotify window detection fails"
**Solution:**
- Make sure Spotify is fully opened
- Not just minimized to tray
- Click on Spotify to ensure it's in foreground

---

## 🎯 Tips for Best Results

### Gesture Recognition:
✅ Collect 100+ training data samples per gesture (not just 50)
✅ Collect in various lighting conditions
✅ Collect from different distances
✅ Use high confidence threshold (keep at 0.6+)

### Spotify Control:
✅ Keep Spotify in focus (or the script will focus it)
✅ Test keyboard shortcuts first (SPACE = play/pause)
✅ Ensure volume keys work on your system
✅ Don't spam gestures too quickly

### Camera Setup:
✅ Position camera at arm level
✅ Good lighting from front (avoid backlighting)
✅ Keep hand 30-60cm from camera
✅ Clear background helps with detection

---

## 📖 File Descriptions

### `spotify_gesture_control.py`
Main application for controlling Spotify with gestures
- Loads trained ML model
- Detects Spotify running
- Processes camera frames
- Sends commands to Spotify
- **Usage:** `python spotify_gesture_control.py`

### `modules/spotify_controller.py`
Low-level Spotify control module
- `is_spotify_running()` - Check if Spotify is active
- `launch_spotify()` - Start Spotify app
- `focus_spotify_window()` - Bring to foreground
- `play_pause()` - Control playback
- `next_track()` / `previous_track()` - Navigate songs
- `volume_up()` / `volume_down()` - Control volume
- `execute_action()` - Execute mapped gesture action

---

## 🔗 Comparison: General vs Spotify

| Feature | General App | Spotify App |
|---------|-------------|-------------|
| **File** | `main_pipeline.py` | `spotify_gesture_control.py` |
| **Module** | `media_controller.py` | `spotify_controller.py` |
| **App Control** | System-wide | Spotify only |
| **Volume Control** | System volume (pycaw) | Media keys |
| **Media Keys** | Generic media | Spotify shortcuts |
| **Window Focus** | Not required | Auto-focuses Spotify |
| **Best For** | Any media app | Spotify users |

---

## 🎓 How It Works (Technical)

### 1. Hand Detection
- MediaPipe detects hand in webcam
- Extracts 21 landmark points

### 2. Feature Extraction
- Calculates 8 features from landmarks
- Distances, angles, finger states

### 3. ML Classification
- Pre-trained Random Forest model
- Predicts gesture class (0-4)
- Returns confidence score

### 4. Action Mapping
- Maps gesture → Spotify action
- Applies confidence threshold
- Smooths with gesture history

### 5. Spotify Control
- Detects Spotify process
- Focuses Spotify window
- Sends keyboard commands
- Applies cooldown

---

## 📝 Customization

### Change gesture to action mapping:
Edit `modules/action_mapper.py`:
```python
DEFAULT_MAPPING = {
    0: VOLUME_UP,           # PALM
    1: VOLUME_DOWN,         # FIST
    2: PLAY_PAUSE,          # PINCH
    3: NEXT_TRACK,          # POINT
    4: PREVIOUS_TRACK,      # V_SIGN
}
```

### Adjust sensitivity:
Edit in `spotify_gesture_control.py`:
```python
SpotifyGestureControl(
    confidence_threshold=0.6  # Lower = more sensitive
)
```

### Change cooldown:
Edit `modules/spotify_controller.py`:
```python
self.action_cooldown = 0.5  # Seconds between actions
```

---

## ✨ Advanced Features

### Check Spotify Status:
```python
from modules.spotify_controller import SpotifyController

spotify = SpotifyController()
status = spotify.get_status()
print(status)
# Output: {'is_running': True, 'process_id': 1234, 'cooldown_active': False}
```

### Launch Spotify from Script:
```python
spotify = SpotifyController()
if not spotify.is_spotify_running():
    spotify.launch_spotify()
```

### Custom Gesture Handling:
```python
from modules.spotify_controller import SpotifyController

spotify = SpotifyController()

# Execute specific actions
spotify.play_pause()
spotify.next_track()
spotify.volume_up()
```

---

## 🎵 Example: Full Integration

```python
import cv2
from modules.hand_detection import HandDetector
from modules.feature_extraction import FeatureExtractor
from modules.gesture_classifier import GestureClassifier
from modules.spotify_controller import SpotifyController

# Initialize components
detector = HandDetector()
extractor = FeatureExtractor()
classifier = GestureClassifier()
classifier.load_model("data/gesture_model_random_forest")
spotify = SpotifyController()

# Main loop
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Detect hand
    frame, landmarks = detector.detect_hands(frame)
    
    if landmarks:
        # Extract features
        features = extractor.extract_features(landmarks[0])
        
        # Predict gesture
        gesture, confidence = classifier.predict(features)
        
        # Control Spotify
        if confidence > 0.6:
            if gesture == 0:  # PALM
                spotify.volume_up()
            elif gesture == 1:  # FIST
                spotify.volume_down()
            elif gesture == 2:  # PINCH
                spotify.play_pause()
    
    cv2.imshow("Spotify Gesture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 📞 Quick Command Reference

| Action | Command |
|--------|---------|
| Install packages | `pip install -r requirements.txt` |
| Check Spotify running | `python` then `from modules.spotify_controller import SpotifyController; s = SpotifyController(); print(s.is_spotify_running())` |
| Run gesture control | `python spotify_gesture_control.py` |
| Run general control | `python main_pipeline.py` |

---

## 🚀 Next Steps

1. ✅ Update requirements: `pip install -r requirements.txt`
2. ✅ Open Spotify
3. ✅ Run: `python spotify_gesture_control.py`
4. ✅ Control Spotify with hand gestures!

---

## 🎉 You're Ready!

Your Spotify gesture control system is complete and ready to use.

**Commands to get started:**

```bash
cd "c:\Users\rithi\OneDrive\Desktop\HAND GESTURE"
.\venv\Scripts\activate
pip install -r requirements.txt
python spotify_gesture_control.py
```

Enjoy controlling Spotify with hand gestures! 🎵🎸🎹

---

**Questions?** Check the troubleshooting section or review the module code.
