# 🎯 Gesture-Controlled Volume & Media Player

## 📋 Project Overview

This is a comprehensive **AI + Computer Vision** project that allows you to control your system volume and media player using hand gestures detected through a webcam. The project uses MediaPipe for hand detection and machine learning models for gesture recognition.

---

## 🧩 Project Architecture

### Module Breakdown:

```
┌─────────────────────────────────────────────────────────┐
│                                                           │
│  📸 CAMERA INPUT                                         │
│         ↓                                                │
│  📌 MODULE 1: Hand Detection (MediaPipe)               │
│         ↓                                                │
│  📊 MODULE 2: Feature Extraction (Distances, Angles)   │
│         ↓                                                │
│  🤖 MODULE 3: Gesture Classification (ML Model)        │
│         ↓                                                │
│  🎯 MODULE 4: Action Mapping (Gesture → Action)        │
│         ↓                                                │
│  🔊 MODULE 5: Media Control (pycaw, pyautogui)         │
│         ↓                                                │
│  ✨ MODULE 6: Real-time Integration (Main Pipeline)    │
│         ↓                                                │
│  📈 MODULE 7: UI Dashboard (Optional)                  │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Supported Gestures

| Gesture | Name | Action |
|---------|------|--------|
| ✋ | PALM | Volume Up |
| ✊ | FIST | Volume Down |
| 🤏 | PINCH | Play/Pause |
| 👉 | POINT | Next Track |
| ✌ | V_SIGN | Previous Track |

---

## 🚀 Quick Start Guide

### Step 1: Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Collect Training Data

```bash
python collect_data.py
```

**Instructions:**
1. Position your hand in front of the camera
2. Press SPACE to capture frames for each gesture
3. Collect 50 samples per gesture (recommended)
4. Press Q when done

### Step 3: Train the Model

```bash
python train_model.py
```

This will:
- Load all collected gesture data
- Train a Random Forest classifier
- Evaluate on test set
- Save the trained model

### Step 4: Run Real-time Control

```bash
python main_pipeline.py
```

**Controls:**
- `Q` - Quit application
- `S` - Toggle settings panel

---

## 📁 Project Structure

```
HAND GESTURE/
│
├── modules/                          # Main modules
│   ├── __init__.py
│   ├── hand_detection.py            # MODULE 1: MediaPipe hand detection
│   ├── feature_extraction.py        # MODULE 2: Feature extraction
│   ├── gesture_classifier.py        # MODULE 3: ML model for classification
│   ├── action_mapper.py             # MODULE 4: Gesture to action mapping
│   └── media_controller.py          # MODULE 5: Volume and media control
│
├── data/                             # Training data and models
│   ├── 0_PALM/                      # Gesture data
│   ├── 1_FIST/
│   ├── 2_PINCH/
│   ├── 3_POINT/
│   ├── 4_V_SIGN/
│   └── gesture_model_random_forest/ # Trained model
│
├── collect_data.py                  # Data collection script
├── train_model.py                   # Model training script
├── main_pipeline.py                 # Real-time gesture control
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── setup.py                         # Installation script
```

---

## 📦 Dependencies

- **opencv-python** - Video capture and image processing
- **mediapipe** - Hand detection and tracking
- **scikit-learn** - Machine learning models (SVM, Random Forest, MLP)
- **numpy** - Numerical computations
- **joblib** - Model serialization
- **pycaw** - Windows audio volume control
- **pyautogui** - Keyboard simulation for media keys

---

## 🔧 Module Details

### Module 1: Hand Detection (`hand_detection.py`)

Uses MediaPipe to detect hands and extract 21 landmark points (knuckles, fingertips, wrist).

**Features:**
- Real-time hand detection (30-60 FPS)
- Returns 21 (x, y, z) coordinates per hand
- Bounding box calculation

**Key Functions:**
- `detect_hands()` - Detect hands in frame
- `get_hand_position()` - Get hand bounding box

### Module 2: Feature Extraction (`feature_extraction.py`)

Extracts meaningful features from hand landmarks for ML model.

**Features Extracted:**
1. Thumb-Index distance (pinch detection)
2. Thumb-Middle distance
3. Finger spread distance
4. Number of fingers open
5. Wrist position (x, y)
6. Angles between fingers
7. Hand size

**Key Functions:**
- `extract_features()` - Extract basic features
- `extract_all_distances()` - Extract all pairwise distances
- `is_finger_open()` - Check if finger is extended

### Module 3: Gesture Classification (`gesture_classifier.py`)

Machine learning model for gesture classification.

**Supported Models:**
- **Random Forest** - Recommended (good balance)
- **SVM** - High accuracy, longer training
- **Neural Network** - Better for complex patterns

**Key Functions:**
- `train()` - Train model on collected data
- `predict()` - Classify gesture from features
- `save_model()` / `load_model()` - Model persistence

### Module 4: Action Mapping (`action_mapper.py`)

Maps detected gestures to media control actions.

**Default Mapping:**
```
PALM (0)    → VOLUME_UP
FIST (1)    → VOLUME_DOWN
PINCH (2)   → PLAY_PAUSE
POINT (3)   → NEXT_TRACK
V_SIGN (4)  → PREVIOUS_TRACK
```

**Customizable:** Easily change gesture-to-action mapping.

### Module 5: Media Control (`media_controller.py`)

Controls system volume and media playback.

**Functions:**
- `get_volume()` / `set_volume()` - Volume control
- `increase_volume()` / `decrease_volume()`
- `play_pause()`, `next_track()`, `previous_track()`
- `execute_action()` - Execute mapped action

**Technical Details:**
- Uses `pycaw` for Windows audio control
- Uses `pyautogui` for media key simulation
- Implements cooldown to prevent gesture spam

### Module 6: Real-time Integration (`main_pipeline.py`)

Combines all modules into a real-time application.

**Pipeline:**
1. Capture frame from camera
2. Detect hand landmarks
3. Extract features
4. Predict gesture
5. Map gesture to action
6. Execute media control
7. Display UI with feedback

---

## 🎓 How It Works

### Data Collection Process:
1. User performs a gesture
2. Hand landmarks are captured
3. Features are extracted and saved
4. Process repeated for all gestures

### Training Process:
1. Load all collected samples
2. Extract features (if not already done)
3. Train ML model (SVM/RF/NN)
4. Evaluate on test set
5. Save model for later use

### Real-time Recognition:
1. Detect hand in each frame
2. Extract features from landmarks
3. Pass features to trained model
4. Get gesture prediction + confidence
5. Only trigger action if confidence > threshold
6. Execute media control action

---

## 💡 Performance Tips

1. **Better Accuracy:**
   - Collect 100+ samples per gesture
   - Vary lighting conditions
   - Vary hand sizes and distances
   - Use multiple people's hands

2. **Faster Processing:**
   - Reduce video resolution
   - Limit to 1 hand detection (already done)
   - Increase confidence threshold

3. **Smoother Gestures:**
   - Increase gesture history size
   - Add smoothing filter
   - Increase cooldown between actions

---

## 🐛 Troubleshooting

### No hand detected:
- Check camera is working
- Ensure good lighting
- Hand should be in center of frame
- Try adjusting hand size

### Gestures not recognized:
- Model may not be trained
- Collected data might be insufficient
- Confidence threshold too high
- Try collecting more varied samples

### Volume control not working:
- On Windows: Requires Windows audio API access
- On Linux: May need additional audio library setup
- Try running with administrator privileges

### Slow performance:
- Reduce camera resolution
- Close other applications
- Update graphics drivers
- Consider using GPU acceleration

---

## 📈 Project Enhancement Ideas

1. **Add More Gestures:**
   - Thumbs up/down
   - Rock gesture
   - OK sign
   - Custom gestures

2. **Better UI:**
   - Tkinter GUI dashboard
   - Web-based interface (Flask/React)
   - Real-time statistics
   - Settings panel

3. **Advanced Features:**
   - Multi-hand gestures
   - Gesture combinations
   - Swipe detection
   - Voice commands integration

4. **Performance:**
   - GPU acceleration with CUDA
   - Model quantization
   - Multi-threading
   - Performance profiling

5. **Applications:**
   - Control presentation slides
   - Game control
   - Home automation
   - VR/AR integration

---

## 📚 Technical Concepts Used

- **MediaPipe Hands** - Real-time hand tracking
- **Feature Engineering** - Extracting meaningful features
- **Machine Learning** - Classification algorithms
- **Real-time Processing** - Frame-by-frame analysis
- **Signal Processing** - Smoothing and filtering
- **Windows API** - Audio control
- **Python** - Main programming language

---

## 🏆 Project Strengths

✅ **Modular Design** - Easy to modify and extend  
✅ **Real-time Performance** - 30-60 FPS  
✅ **No Training Data Needed Initially** - Can customize  
✅ **Easy to Demonstrate** - Impressive for presentations  
✅ **Scalable** - Can add more gestures easily  
✅ **Customizable** - All parameters adjustable  

---

## 📝 Project Report Structure

For your academic report:

1. **Introduction** - Project overview and motivation
2. **Literature Review** - MediaPipe, ML models, gesture recognition
3. **System Architecture** - 7 modules explanation
4. **Implementation** - Code walkthrough
5. **Results** - Model accuracy, performance metrics
6. **Conclusion** - Summary and future work

---

## 🤝 Contributing

Feel free to extend this project with:
- New gesture types
- Better UI
- Additional models
- Performance optimizations
- Documentation improvements

---

## 📄 License

This project is created for educational purposes.

---

## ✨ Keywords for Your Project

Hand Gesture Recognition | Computer Vision | MediaPipe | Machine Learning | 
Real-time Processing | Gesture Classification | Media Control | Audio Control | 
Python | Scikit-learn | OpenCV | AI | AIML

---

**Good luck with your project! 🚀**
