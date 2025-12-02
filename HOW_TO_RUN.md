# 🚀 HOW TO RUN - QUICK GUIDE

## ⚡ Super Quick Start (30 seconds)

```bash
# Open PowerShell and navigate to project
cd "c:\Users\rithi\OneDrive\Desktop\HAND GESTURE"

# Activate virtual environment
.\venv\Scripts\activate

# Run the gesture control
python main_pipeline.py
```

**That's it! You're now controlling volume with hand gestures!** 🎉

---

## 📋 Complete Step-by-Step Instructions

### **FIRST TIME SETUP (15 minutes)**

#### Step 1️⃣: Open PowerShell
```bash
# Open Windows PowerShell or Command Prompt
# Navigate to project directory
cd "c:\Users\rithi\OneDrive\Desktop\HAND GESTURE"
```

#### Step 2️⃣: Create Virtual Environment
```bash
# Create virtual environment (first time only)
python -m venv venv

# Activate it
.\venv\Scripts\activate

# You should see (venv) at the start of your terminal
```

#### Step 3️⃣: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Wait for it to complete (2-3 minutes)
# You'll see ✓ Successfully installed at the end
```

---

### **COLLECT TRAINING DATA (15 minutes)**

```bash
# Make sure you're in the project directory with venv activated
python collect_data.py
```

**What to do:**
1. Position your hand in front of camera
2. For each gesture, press SPACE to capture 50 frames:
   - ✋ **PALM** - Open hand, all fingers extended
   - ✊ **FIST** - Closed fist, all fingers folded
   - 🤏 **PINCH** - Thumb and index finger together
   - 👉 **POINT** - Index finger pointing straight up
   - ✌ **V_SIGN** - Peace sign (two fingers)
3. Press Q when done

**Tips:**
- Good lighting is important
- Vary hand distance (30-60cm from camera)
- Vary angles and orientations
- Collect in different backgrounds for better accuracy

---

### **TRAIN THE MODEL (1 minute)**

```bash
# Train machine learning model on collected data
python train_model.py
```

**What happens:**
- Loads your collected data (250 samples)
- Trains Random Forest classifier
- Shows accuracy: ~90-95%
- Saves model automatically

**Expected output:**
```
Loading training data...
✓ Loaded dataset: 250 samples, 8 features
🔧 Training random_forest model...
Training accuracy: 95.00%
📈 Model Evaluation:
   Test accuracy: 91.00%
✓ Model saved successfully!
```

---

### **RUN REAL-TIME GESTURE CONTROL (Unlimited)**

```bash
# Start gesture-controlled media player
python main_pipeline.py
```

**What you'll see:**
- Live video from your camera
- Hand detection with landmarks
- Detected gesture name
- Confidence score
- Volume level indicator
- FPS counter

**Controls:**
- Show your hand to detect gestures
- Different gestures = different actions
- **Q** = Quit application
- **S** = Toggle settings panel

**Actions triggered:**
- ✋ **PALM** → Volume Up
- ✊ **FIST** → Volume Down
- 🤏 **PINCH** → Play/Pause
- 👉 **POINT** → Next Track
- ✌ **V_SIGN** → Previous Track

---

## 🔄 RUNNING AGAIN (Next Time)

After first setup, you only need:

```bash
# Open PowerShell in project directory
cd "c:\Users\rithi\OneDrive\Desktop\HAND GESTURE"

# Activate virtual environment
.\venv\Scripts\activate

# Run gesture control directly
python main_pipeline.py
```

**No need to reinstall or retrain!**

---

## 🧪 TESTING BEFORE RUNNING

If you want to verify everything works:

```bash
# Test camera, hand detection, and features
python test_modules.py
```

This runs 3 quick tests:
- ✅ Camera detection
- ✅ Hand detection (MediaPipe)
- ✅ Feature extraction

All should show "PASSED" ✓

---

## 🆘 TROUBLESHOOTING

### ❌ "Command not found: python"
**Solution:**
- Add Python to PATH during reinstallation
- Or use `python3` instead of `python`

### ❌ "ModuleNotFoundError: No module named 'mediapipe'"
**Solution:**
```bash
# Make sure venv is activated (should see (venv) in terminal)
pip install -r requirements.txt
```

### ❌ "Camera not found"
**Solution:**
- Check if webcam is physically connected
- Grant camera permissions to PowerShell
- Try running in administrator mode

### ❌ "No hand detected"
**Solution:**
- Ensure good lighting
- Keep hand centered in camera
- Keep hand 30-60cm from camera
- Collect more training data

### ❌ "Accuracy too low (< 80%)"
**Solution:**
- Collect 100+ samples per gesture instead of 50
- Vary lighting conditions
- Vary hand orientations
- Delete old data and recollect

### ❌ "Volume control not working"
**Solution:**
- Run PowerShell as Administrator
- Windows: Audio service must be running
- Restart the application

---

## 📊 QUICK COMMAND REFERENCE

| What You Want | Command |
|---------------|---------|
| Setup (first time) | `python quick_start.py` |
| Navigate to folder | `cd "c:\Users\rithi\OneDrive\Desktop\HAND GESTURE"` |
| Activate venv | `.\venv\Scripts\activate` |
| Install dependencies | `pip install -r requirements.txt` |
| Test components | `python test_modules.py` |
| Collect data | `python collect_data.py` |
| Train model | `python train_model.py` |
| Run live control | `python main_pipeline.py` |
| Deactivate venv | `deactivate` |

---

## 🎯 TYPICAL WORKFLOW

**First Time:**
```bash
cd "c:\Users\rithi\OneDrive\Desktop\HAND GESTURE"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python collect_data.py          # 15 min
python train_model.py           # 1 min
python main_pipeline.py         # Use it!
```

**Next Time (Just run):**
```bash
cd "c:\Users\rithi\OneDrive\Desktop\HAND GESTURE"
.\venv\Scripts\activate
python main_pipeline.py         # Done!
```

---

## ⚙️ CUSTOMIZATION

### Change gesture actions:
Edit `modules/action_mapper.py` - change the GESTURE_MAPPING

### Adjust sensitivity:
Edit `config.py` - change `confidence_threshold` (lower = more sensitive)

### Change volume step:
Edit `config.py` - change `volume_step` (default 0.05 = 5%)

### Use different ML model:
In `main_pipeline.py`, change:
```python
GestureControlPipeline(
    model_path="data/gesture_model_svm",  # or "gesture_model_neural_network"
)
```

---

## 📱 KEYBOARD SHORTCUTS (While Running)

| Key | Action |
|-----|--------|
| **Q** | Quit application |
| **S** | Toggle settings panel |
| **SPACE** (in collect_data) | Capture frame |

---

## ✨ EXPECTED RESULTS

### After Setup:
- Virtual environment created ✓
- All dependencies installed ✓
- Camera working ✓

### After Data Collection:
- 250 training samples collected ✓
- 5 gesture directories populated ✓
- Ready for training ✓

### After Training:
- Model trained successfully ✓
- Test accuracy: 90-95% ✓
- Model saved (.pkl file) ✓

### During Live Control:
- Hand detected in real-time ✓
- Gestures recognized correctly ✓
- Volume changes smoothly ✓
- Media controls respond ✓
- 30-60 FPS performance ✓

---

## 🎓 NEXT STEPS

1. ✅ Run through setup once
2. ✅ Collect training data (50 per gesture)
3. ✅ Train model (automatic)
4. ✅ Test real-time control
5. 📈 Improve accuracy by collecting more data
6. 🔧 Customize in `config.py`
7. 📖 Read `README.md` for advanced topics

---

## 📞 QUICK TIPS

- **Always activate venv first** before running scripts
- **Collect diverse data** for better accuracy
- **Good lighting is critical** for hand detection
- **Keep 30-60cm from camera** - not too close, not too far
- **Edit config.py** to customize behavior
- **Run test_modules.py** to verify setup

---

**You're all set! Run `python main_pipeline.py` to start! 🚀**
