"""
COMPLETE INSTALLATION AND SETUP GUIDE
Step-by-step instructions for Windows, Linux, and macOS
"""

# ============================================================================
#                        INSTALLATION GUIDE
# ============================================================================

SETUP_GUIDE = """
═════════════════════════════════════════════════════════════════════════════

  GESTURE-CONTROLLED MEDIA PLAYER - SETUP GUIDE
                                                
═════════════════════════════════════════════════════════════════════════════

PROJECT REQUIREMENTS:
- Python 3.8 or higher
- Webcam (built-in or USB)
- 4GB RAM (8GB recommended)
- Windows/Linux/macOS

ESTIMATED TIME: 10-15 minutes

============================================================================
STEP 1: VERIFY PYTHON INSTALLATION
============================================================================

Open Command Prompt/PowerShell/Terminal and run:

    python --version

If this shows "Python 3.8+" then proceed.
If not, download from https://www.python.org/downloads/

⚠️  IMPORTANT for Windows: During installation, CHECK "Add Python to PATH"

============================================================================
STEP 2: NAVIGATE TO PROJECT DIRECTORY
============================================================================

Windows (PowerShell):
    cd "c:\\Users\\rithi\\OneDrive\\Desktop\\HAND GESTURE"

Linux/macOS (Terminal):
    cd ~/Desktop/"HAND GESTURE"

Verify you see:
    - modules/
    - data/
    - collect_data.py
    - train_model.py
    - etc.

============================================================================
STEP 3: CREATE VIRTUAL ENVIRONMENT
============================================================================

Windows (PowerShell):
    python -m venv venv
    .\\venv\\Scripts\\activate

Linux/macOS (Terminal):
    python3 -m venv venv
    source venv/bin/activate

Expected: You should see (venv) prefix in your terminal

============================================================================
STEP 4: UPGRADE PIP
============================================================================

    python -m pip install --upgrade pip

This ensures you have the latest package installer.

============================================================================
STEP 5: INSTALL DEPENDENCIES
============================================================================

    pip install -r requirements.txt

This will install:
    ✓ opencv-python
    ✓ mediapipe
    ✓ numpy
    ✓ scikit-learn
    ✓ joblib
    ✓ pycaw (Windows only for volume control)
    ✓ pyautogui

⏱️  This may take 3-5 minutes depending on your internet speed.

============================================================================
STEP 6: VERIFY INSTALLATION
============================================================================

Run the test script:
    python test_modules.py

This will test:
    ✓ Camera detection
    ✓ MediaPipe hand detection
    ✓ Feature extraction

If all tests pass, you're ready to proceed!

============================================================================
STEP 7: COLLECT TRAINING DATA
============================================================================

Run:
    python collect_data.py

Instructions:
    1. Position your hand in front of the camera
    2. Press SPACE to capture frames for each gesture
    3. Collect at least 50 samples per gesture
    4. Total: ~250 samples for 5 gestures
    5. Take ~10-15 minutes

GESTURES TO COLLECT:
    ✋ PALM        - Open hand (all fingers extended)
    ✊ FIST        - Closed fist (all fingers folded)
    🤏 PINCH       - Thumb and index finger together
    👉 POINT       - Index finger pointing up
    ✌  V_SIGN      - Peace sign (two fingers)

Tips:
    • Collect in good lighting
    • Vary hand distance from camera (30-50cm)
    • Vary hand orientation (different angles)
    • Try different backgrounds
    • The more diverse, the better the accuracy!

============================================================================
STEP 8: TRAIN THE MODEL
============================================================================

Run:
    python train_model.py

This will:
    ✓ Load your collected data
    ✓ Train Random Forest classifier
    ✓ Evaluate accuracy
    ✓ Save the model

Expected output:
    ✓ Loaded dataset: 250 samples, 8 features
    ✓ Classes: 5
    Training accuracy: ~95%
    Test accuracy: ~90%

⏱️  Training takes ~30 seconds

============================================================================
STEP 9: TEST REAL-TIME CONTROL
============================================================================

Run:
    python main_pipeline.py

Controls:
    ✓ Show your hand and see it detected
    ✓ Different gestures should trigger different actions
    ✓ Watch volume bar change
    ✓ Press 'Q' to quit
    ✓ Press 'S' to see settings

First run checklist:
    ☐ Hand is detected (green text appears)
    ☐ Gesture name is shown
    ☐ Confidence score is displayed
    ☐ Volume level is shown
    ☐ Actions are executed on your system

============================================================================
TROUBLESHOOTING
============================================================================

❌ Camera not detected:
   → Check if webcam is working (try Skype, Discord)
   → Grant camera permissions to Python
   → Restart the application

❌ No gestures recognized:
   → Collect more training data (100+ per gesture)
   → Ensure varied lighting conditions
   → Check confidence threshold in config.py

❌ Volume control not working:
   → Windows: Run with administrator privileges
   → Linux: Install audio library
   → macOS: Check system permissions

❌ ImportError for mediapipe:
   → pip uninstall mediapipe
   → pip install mediapipe --upgrade

❌ "Module not found" errors:
   → Make sure venv is activated
   → Run from project root directory
   → Check requirements.txt is in correct location

============================================================================
FILE STRUCTURE AFTER SETUP
============================================================================

After completing all steps, your directory should look like:

    HAND GESTURE/
    ├── modules/
    │   ├── hand_detection.py
    │   ├── feature_extraction.py
    │   ├── gesture_classifier.py
    │   ├── action_mapper.py
    │   └── media_controller.py
    ├── data/
    │   ├── 0_PALM/ (with .npy files)
    │   ├── 1_FIST/ (with .npy files)
    │   ├── 2_PINCH/ (with .npy files)
    │   ├── 3_POINT/ (with .npy files)
    │   ├── 4_V_SIGN/ (with .npy files)
    │   ├── gesture_model_random_forest.pkl ✓
    │   └── gesture_model_random_forest_scaler.pkl ✓
    ├── venv/
    ├── collect_data.py
    ├── train_model.py
    ├── main_pipeline.py
    ├── requirements.txt
    └── ...other files...

============================================================================
QUICK COMMANDS SUMMARY
============================================================================

Setup (first time only):
    python -m venv venv
    .\\venv\\Scripts\\activate          # Windows
    source venv/bin/activate           # Linux/macOS
    pip install -r requirements.txt

Always activate virtual environment before running:
    .\\venv\\Scripts\\activate          # Windows
    source venv/bin/activate           # Linux/macOS

Run setup wizard:
    python quick_start.py

Test components:
    python test_modules.py

Collect training data:
    python collect_data.py

Train model:
    python train_model.py

Run gesture control:
    python main_pipeline.py

Deactivate virtual environment (when done):
    deactivate

============================================================================
NEXT STEPS
============================================================================

1. ✅ Install dependencies
2. ✅ Verify installation
3. ✅ Collect training data
4. ✅ Train the model
5. ✅ Run real-time control
6. 📖 Read README.md for advanced usage
7. 🔧 Customize in config.py
8. 📊 Improve model with more data

============================================================================
SUPPORT
============================================================================

If you encounter issues:

1. Check the error message carefully
2. Ensure Python 3.8+
3. Verify all dependencies installed
4. Check if webcam is working
5. Try running test_modules.py
6. Review ARCHITECTURE.md for technical details

============================================================================

Ready to proceed? Run:

    python collect_data.py

Good luck! 🚀
"""

if __name__ == "__main__":
    print(SETUP_GUIDE)
