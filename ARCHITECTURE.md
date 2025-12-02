# 🏗️ ARCHITECTURE DOCUMENTATION

## Project Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                 GESTURE-CONTROLLED MEDIA PLAYER                 │
│                      (AI + Computer Vision)                     │
└─────────────────────────────────────────────────────────────────┘

                           SYSTEM PIPELINE
                           
┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│  📸 INPUT: Webcam Feed (30-60 FPS)                              │
│                    ↓                                             │
│  MODULE 1: Hand Detection (MediaPipe Hands)                     │
│  ├─ Detects hand presence in frame                             │
│  ├─ Extracts 21 3D landmark points                             │
│  ├─ Returns: landmarks_list (n_hands, 21, 3)                  │
│                    ↓                                             │
│  MODULE 2: Feature Extraction                                   │
│  ├─ Calculates distances between landmarks                     │
│  ├─ Computes angles between joints                             │
│  ├─ Determines finger states                                   │
│  ├─ Returns: feature_vector (1, 8-15)                         │
│                    ↓                                             │
│  MODULE 3: Gesture Classification (ML Model)                    │
│  ├─ Uses trained Random Forest/SVM/NN                          │
│  ├─ Predicts gesture class (0-4)                               │
│  ├─ Returns: gesture_class, confidence                         │
│                    ↓                                             │
│  Confidence Filtering (threshold = 0.6)                         │
│  ├─ If confidence < threshold: SKIP action                     │
│  ├─ If confidence ≥ threshold: PROCEED                         │
│                    ↓                                             │
│  Gesture Smoothing (history buffer)                             │
│  ├─ Keep last 5 predictions                                    │
│  ├─ Use majority vote for stability                            │
│                    ↓                                             │
│  MODULE 4: Action Mapping                                       │
│  ├─ Map gesture → media action                                 │
│  ├─ Returns: action (volume_up, play_pause, etc.)             │
│                    ↓                                             │
│  Action Cooldown (0.3 seconds)                                  │
│  ├─ Prevent duplicate action triggering                        │
│  ├─ Allow only one action per 0.3 seconds                      │
│                    ↓                                             │
│  MODULE 5: Media Controller                                     │
│  ├─ Execute volume control (pycaw)                             │
│  ├─ Send media key presses (pyautogui)                         │
│  ├─ Update system state                                        │
│                    ↓                                             │
│  MODULE 6: UI Renderer                                          │
│  ├─ Display gesture name                                       │
│  ├─ Show confidence score                                      │
│  ├─ Draw volume indicator                                      │
│  ├─ Show FPS counter                                           │
│                    ↓                                             │
│  🔊 OUTPUT: Volume & Media Control                              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Dependency Graph

```
                    ┌──────────────┐
                    │   Webcam     │
                    └──────┬───────┘
                           │
                    ┌──────▼──────────┐
                    │ hand_detection  │◄─── MediaPipe
                    │   MODULE 1      │
                    └──────┬──────────┘
                           │ landmarks[0] = 21 points
                    ┌──────▼──────────────┐
                    │feature_extraction   │
                    │   MODULE 2          │
                    └──────┬──────────────┘
                           │ features[8]
                    ┌──────▼──────────────┐
                    │gesture_classifier   │◄─── scikit-learn
                    │   MODULE 3          │     (trained model)
                    └──────┬──────────────┘
                           │ gesture_class, confidence
                    ┌──────▼──────────────┐
                    │  action_mapper      │◄─── config.py
                    │   MODULE 4          │
                    └──────┬──────────────┘
                           │ action (string)
                    ┌──────▼──────────────┐
                    │ media_controller    │◄─── pycaw, pyautogui
                    │   MODULE 5          │
                    └──────┬──────────────┘
                           │
                ┌──────────┴──────────┐
                │                    │
        ┌───────▼────────┐   ┌───────▼────────┐
        │ Volume Control │   │ Media Control  │
        │   (pycaw)      │   │   (pyautogui)  │
        └────────────────┘   └────────────────┘
                │                    │
                └──────────┬─────────┘
                           │
                    ┌──────▼──────────┐
                    │ System Audio &  │
                    │    Media Apps   │
                    └─────────────────┘
```

---

## Data Flow Diagram

```
FRAME PROCESSING PIPELINE (per frame):

Input Frame (BGR, 640x480)
    │
    ├─► MediaPipe Hand Detection
    │   ├─ Hand Present? NO ──► Skip to next frame
    │   └─ Hand Present? YES ─┐
    │                         │
    │     Extract 21 Landmarks (x, y, z) per hand
    │     └─ landmarks: array(21, 3)
    │
    ├─► Feature Extraction
    │   ├─ Thumb-Index distance
    │   ├─ All finger distances
    │   ├─ Number of open fingers
    │   ├─ Wrist position
    │   ├─ Joint angles
    │   └─ features: array(8,)
    │
    ├─► Gesture Classification
    │   ├─ Scale features (normalize)
    │   ├─ Feed to ML model
    │   ├─ Get predictions for all classes
    │   ├─ Select highest probability
    │   └─ gesture_class: 0-4, confidence: 0.0-1.0
    │
    ├─ Confidence > threshold? NO ──► Skip action
    │  \ YES
    │
    ├─► Gesture Smoothing
    │   ├─ Add to history buffer (size=5)
    │   ├─ Majority vote
    │   └─ stable_gesture: 0-4
    │
    ├─► Action Mapping
    │   ├─ Look up: gesture → action
    │   └─ action: 'volume_up' | 'play_pause' | etc.
    │
    ├─ Cooldown elapsed? NO ──► Skip execution
    │  \ YES
    │
    ├─► Media Control Execution
    │   └─ Execute system action
    │
    └─► UI Rendering
        ├─ Draw gesture name
        ├─ Show confidence %
        ├─ Display volume bar
        ├─ Show FPS counter
        └─ Display frame


TIMING ANALYSIS (per frame @ 30 FPS = 33.3ms per frame):

                                    Time (ms)    Budget
    ┌─ Hand Detection           2-5 ms       ◄─ ~17%
    ├─ Feature Extraction       1-2 ms       ◄─ ~5%
    ├─ Model Prediction         1-3 ms       ◄─ ~9%
    ├─ Gesture Smoothing        <1 ms        ◄─ ~3%
    ├─ Action Mapping           <1 ms        ◄─ ~3%
    ├─ Media Control            <1 ms        ◄─ ~3%
    ├─ UI Rendering             3-5 ms       ◄─ ~15%
    └─ Buffer/Display          5-10 ms       ◄─ ~30%
        ────────────────────────────────
        TOTAL:                 15-30 ms      (30-60 FPS achieved)
```

---

## Class Hierarchy

```
HandDetector
├─ Attributes:
│  ├─ hands (MediaPipe Hands object)
│  ├─ mp_hands (MediaPipe solutions)
│  └─ max_hands, detection_con, tracking_con
│
└─ Methods:
   ├─ detect_hands(frame) → (frame, landmarks_list)
   └─ get_hand_position(landmarks) → (x_min, y_min, x_max, y_max, w, h)


FeatureExtractor
├─ Attributes:
│  └─ landmarks (current hand landmarks)
│
└─ Methods:
   ├─ distance(p1, p2) → float
   ├─ angle_between_points(p1, p2, p3) → float (degrees)
   ├─ is_finger_open(tip, pip) → bool
   ├─ extract_features(landmarks) → array(8,)
   └─ extract_all_distances(landmarks) → array(n,)


GestureClassifier
├─ Attributes:
│  ├─ model (SVM/RF/MLP)
│  ├─ scaler (StandardScaler)
│  ├─ model_type (string)
│  └─ is_trained (bool)
│
└─ Methods:
   ├─ train(X_train, y_train)
   ├─ predict(features) → (gesture_class, confidence)
   ├─ predict_batch(X) → (predictions, confidences)
   ├─ save_model(path)
   ├─ load_model(path)
   └─ get_gesture_name(class) → string


ActionMapper
├─ Attributes:
│  ├─ mapping (dict: gesture → action)
│  ├─ last_action
│  └─ action_counter
│
└─ Methods:
   ├─ get_action(gesture) → string
   ├─ set_custom_mapping(gesture, action)
   ├─ reset_mapping()
   ├─ get_mapping() → dict
   └─ get_action_description(action) → string


MediaController
├─ Attributes:
│  ├─ volume_control (Windows audio API)
│  ├─ current_volume
│  ├─ last_action_time
│  └─ action_cooldown
│
└─ Methods:
   ├─ get_volume() → float (0.0-1.0)
   ├─ set_volume(volume)
   ├─ increase_volume(step)
   ├─ decrease_volume(step)
   ├─ play_pause()
   ├─ next_track()
   ├─ previous_track()
   ├─ execute_action(action)
   └─ _check_cooldown() → bool


GestureControlPipeline
├─ Attributes:
│  ├─ hand_detector
│  ├─ feature_extractor
│  ├─ gesture_classifier
│  ├─ action_mapper
│  ├─ media_controller
│  ├─ gesture_history
│  └─ confidence_threshold
│
└─ Methods:
   ├─ process_frame(frame) → (frame, gesture, confidence)
   ├─ run(camera_id)
   ├─ _draw_ui(frame, gesture, confidence, action)
   └─ _draw_settings(frame)
```

---

## File Organization

```
HAND GESTURE/
│
├── 📁 modules/                          # Core modules
│   ├── __init__.py
│   ├── hand_detection.py               (Module 1)
│   ├── feature_extraction.py           (Module 2)
│   ├── gesture_classifier.py           (Module 3)
│   ├── action_mapper.py                (Module 4)
│   └── media_controller.py             (Module 5)
│
├── 📁 data/                            # Training data and models
│   ├── 0_PALM/
│   │   ├── features_0.npy
│   │   ├── landmarks_0.npy
│   │   └── ...
│   ├── 1_FIST/
│   ├── 2_PINCH/
│   ├── 3_POINT/
│   ├── 4_V_SIGN/
│   ├── gesture_model_random_forest.pkl
│   └── gesture_model_random_forest_scaler.pkl
│
├── 🐍 collect_data.py                 (Data collection)
├── 🐍 train_model.py                  (Training script)
├── 🐍 main_pipeline.py                (Module 6 - Real-time control)
├── 🐍 test_modules.py                 (Testing utility)
├── 🐍 quick_start.py                  (Setup wizard)
├── 🐍 config.py                       (Configuration)
├── 🐍 setup.py                        (Installation)
│
├── 📄 README.md                       (Full documentation)
├── 📄 PROJECT_SUMMARY.md              (Project overview)
├── 📄 ARCHITECTURE.md                 (This file)
└── 📄 requirements.txt                (Dependencies)
```

---

## Integration Points

### 1. Camera Input
- OpenCV (`cv2.VideoCapture`)
- Feeds raw frames to HandDetector

### 2. Hand Detection
- MediaPipe Hands API
- Outputs landmark coordinates

### 3. ML Inference
- Scikit-learn models (Random Forest/SVM/MLP)
- Takes extracted features, returns prediction

### 4. Media Control
- Windows API (pycaw for volume)
- System keyboard (pyautogui for media keys)
- Sends commands to OS

### 5. UI Display
- OpenCV drawing functions
- Displays live feedback

---

## Performance Characteristics

| Component | Latency | Throughput |
|-----------|---------|-----------|
| Hand Detection | 3-5ms | 60 FPS |
| Feature Extraction | 1-2ms | 500+ FPS |
| ML Prediction | 1-3ms | 300+ FPS |
| Media Control | <1ms | 1000+ ops/sec |
| **Total (per frame)** | **15-30ms** | **30-60 FPS** |

---

## Error Handling

```
Main Pipeline Error Flow:

┌─ Camera Error
├─→ Caught: Display error message
├─→ Recovery: Retry camera initialization

┌─ Model Not Found
├─→ Caught: FileNotFoundError
├─→ Recovery: Prompt to train model first

┌─ Low Confidence Prediction
├─→ Caught: Check threshold
├─→ Recovery: Skip action, continue

┌─ Audio Control Error
├─→ Caught: pycaw exception
├─→ Recovery: Log error, continue without volume control

┌─ Feature Extraction Error
├─→ Caught: Invalid landmarks
├─→ Recovery: Skip frame, get next hand
```

---

## System Requirements

- **OS:** Windows 10/11, Linux, macOS
- **Python:** 3.8+
- **RAM:** 4GB minimum (8GB recommended)
- **GPU:** Optional (CPU sufficient for 30 FPS)
- **Camera:** USB webcam, 30+ FPS capable
- **Internet:** Minimal (only for pip install)

---

This architecture is designed for:
✅ **Modularity** - Easy to modify components  
✅ **Extensibility** - Easy to add features  
✅ **Performance** - Real-time processing  
✅ **Reliability** - Error handling throughout  
✅ **Maintainability** - Clean, documented code  
