echo.
echo Creating simple_gesture_spotify.py...
echo.

(
echo """
🎵 SIMPLE GESTURE SPOTIFY CONTROL (No MediaPipe Required)
Uses OpenCV contour detection for basic gesture recognition
"""

echo import cv2
echo import numpy as np
echo import pyautogui
echo import time
echo import subprocess
echo import psutil
echo import os

echo print("🎵 Starting Simple Gesture Spotify Control...")

echo "# ================================"
echo "# 🎵 SPOTIFY LAUNCHER"
echo "# ================================"

echo def launch_spotify():
echo     """Launch Spotify in a separate window"""
echo     print("🚀 Launching Spotify...")
echo.
echo     try:
echo         "# Try multiple ways to open Spotify"
echo         spotify_paths = [
echo             r"C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe".format(os.getenv('USERNAME')),
echo             r"C:\Program Files\Spotify\Spotify.exe",
echo             "spotify"  "# Command line"
echo         ]
echo.
echo         for path in spotify_paths:
echo             try:
echo                 subprocess.Popen(path, shell=True)
echo                 print(f"✅ Spotify launched from: {path}")
echo                 break
echo             except:
echo                 continue
echo         else:
echo             "# Final fallback"
echo             os.system("start spotify:")
echo             print("✅ Spotify launched via system command")
echo.
echo         "# Wait for Spotify to load"
echo         time.sleep(5)
echo         return True
echo.
echo     except Exception as e:
echo         print(f"❌ Error launching Spotify: {e}")
echo         return False

echo def is_spotify_running():
echo     """Check if Spotify is running"""
echo     try:
echo         for proc in psutil.process_iter(['name']):
echo             if 'spotify' in proc.info['name'].lower():
echo                 return True
echo         return False
echo     except:
echo         return False

echo "# ================================"
echo "# ✋ SIMPLE HAND DETECTION (No MediaPipe)"
echo "# ================================"

echo class SimpleHandDetector:
echo     def __init__(self):
echo         self.background = None
echo         self.bg_captured = False
echo.
echo     def capture_background(self, frame):
echo         """Capture background for subtraction"""
echo         self.background = cv2.GaussianBlur(frame, (21, 21), 0)
echo         self.bg_captured = True
echo         print("✅ Background captured for hand detection")
echo.
echo     def detect_hand_contour(self, frame):
echo         """Detect hand using background subtraction and contour analysis"""
echo         if not self.bg_captured:
echo             self.capture_background(frame)
echo             return None, "Capturing background..."
echo.
echo         "# Preprocess frame"
echo         blurred = cv2.GaussianBlur(frame, (21, 21), 0)
echo         diff = cv2.absdiff(self.background, blurred)
echo.
echo         "# Convert to grayscale and threshold"
echo         gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
echo         _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
echo.
echo         "# Morphological operations to clean up"
echo         kernel = np.ones((5, 5), np.uint8)
echo         thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
echo         thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
echo.
echo         "# Find contours"
echo         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
echo.
echo         if not contours:
echo             return None, "No hand detected"
echo.
echo         "# Find largest contour (likely hand)"
echo         largest_contour = max(contours, key=cv2.contourArea)
echo.
echo         "# Filter by area (avoid small noise)"
echo         area = cv2.contourArea(largest_contour)
echo         if area < 1000:  "# Minimum hand area"
echo             return None, "Hand too small"
echo.
echo         return largest_contour, f"Hand detected: {int(area)}px"
echo.
echo     def detect_gesture_simple(self, contour, frame):
echo         """Simple gesture detection based on contour shape"""
echo         if contour is None:
echo             return "no_hand", "❌"
echo.
echo         "# Get contour features"
echo         hull = cv2.convexHull(contour)
echo         hull_area = cv2.contourArea(hull)
echo         contour_area = cv2.contourArea(contour)
echo.
echo         "# Calculate solidity (area ratio)"
echo         solidity = float(contour_area) / hull_area if hull_area > 0 else 0
echo.
echo         "# Get bounding rectangle"
echo         x, y, w, h = cv2.boundingRect(contour)
echo         aspect_ratio = float(w) / h
echo.
echo         "# Simple gesture classification"
echo         if solidity > 0.9:
echo             return "fist", "✊"  "# Closed fist (high solidity)"
echo         elif aspect_ratio > 1.2:
echo             return "palm", "🖐️"  "# Wide palm"
echo         elif aspect_ratio < 0.8:
echo             return "point", "☝️"  "# Tall/pointing"
echo         else:
echo             return "hand", "👋"  "# Generic hand"

echo "# ================================"
echo "# 🎮 GESTURE CONTROLS"
echo "# ================================"

echo class GestureController:
echo     def __init__(self):
echo         self.last_action_time = 0
echo         self.action_cooldown = 2.0  "# Prevent spam"
echo         self.last_gesture = None
echo.
echo     def execute_gesture(self, gesture):
echo         """Execute Spotify control based on gesture"""
echo         current_time = time.time()
echo.
echo         "# Cooldown check"
echo         if current_time - self.last_action_time < self.action_cooldown:
echo             return False
echo.
echo         "# Don't repeat same gesture immediately"
echo         if gesture == self.last_gesture:
echo             return False
echo.
echo         self.last_gesture = gesture
echo         self.last_action_time = current_time
echo.
echo         "# Gesture to action mapping"
echo         actions = {
echo             "palm": self.play_pause,
echo             "fist": self.play_pause,
echo             "point": self.next_track,
echo             "hand": self.previous_track,
echo         }
echo.
echo         action_func = actions.get(gesture)
echo         if action_func:
echo             action_func()
echo             return True
echo.
echo         return False
echo.
echo     def play_pause(self):
echo         pyautogui.press('space')
echo         print("🎵 Play/Pause")
echo.
echo     def next_track(self):
echo         pyautogui.hotkey('ctrl', 'right')
echo         print("⏭️ Next Track")
echo.
echo     def previous_track(self):
echo         pyautogui.hotkey('ctrl', 'left')
echo         print("⏮️ Previous Track")
echo.
echo     def volume_up(self):
echo         pyautogui.press('volumeup')
echo         print("🔊 Volume Up")
echo.
echo     def volume_down(self):
echo         pyautogui.press('volumedown')
echo         print("🔉 Volume Down")

echo "# ================================"
echo "# 🚀 MAIN APPLICATION"
echo "# ================================"

echo def main():
echo     print("🎵 SIMPLE GESTURE SPOTIFY CONTROL")
echo     print("=================================")
echo     print("📋 This version uses basic computer vision")
echo     print("📋 No MediaPipe required!")
echo.
echo     "# Step 1: Launch or check Spotify"
echo     if not is_spotify_running():
echo         print("📋 Step 1: Launching Spotify...")
echo         if not launch_spotify():
echo             print("❌ Please open Spotify MANUALLY and play some music")
echo             print("   Then press Enter to continue...")
echo             input()
echo     else:
echo         print("✅ Spotify is already running!")
echo.
echo     "# Step 2: Initialize camera"
echo     print("📋 Step 2: Starting camera...")
echo     cap = cv2.VideoCapture(0)
echo     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
echo     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
echo.
echo     if not cap.isOpened():
echo         print("❌ Cannot open camera!")
echo         return
echo.
echo     hand_detector = SimpleHandDetector()
echo     gesture_controller = GestureController()
echo.
echo     print("📋 Step 3: Starting gesture control...")
echo     print("\n🎮 SIMPLE GESTURE CONTROLS:")
echo     print("🖐️  OPEN PALM (wide shape) → Play/Pause")
echo     print("✊  FIST (compact shape) → Play/Pause") 
echo     print("☝️  POINTING (tall shape) → Next Track")
echo     print("👋  GENERIC HAND → Previous Track")
echo     print("\n💡 TIPS:")
echo     print("- Make sure your hand contrasts with background")
echo     print("- Use consistent lighting")
echo     print("- Keep hand still for better detection")
echo     print("- Press 'C' to recapture background")
echo     print("- Press 'Q' to quit")
echo     print("=" * 50)
echo.
echo     background_captured = False
echo.
echo     try:
echo         while True:
echo             ret, frame = cap.read()
echo             if not ret:
echo                 print("❌ Camera error")
echo                 break
echo.
echo             "# Mirror effect"
echo             frame = cv2.flip(frame, 1)
echo.
echo             "# Detect hand and gesture"
echo             contour, status = hand_detector.detect_hand_contour(frame)
echo             gesture, emoji = hand_detector.detect_gesture_simple(contour, frame)
echo.
echo             "# Execute gesture action"
echo             if gesture != "no_hand":
echo                 gesture_controller.execute_gesture(gesture)
echo.
echo             "# Draw visualization"
echo             if contour is not None:
echo                 cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
echo.
echo                 "# Draw bounding box"
echo                 x, y, w, h = cv2.boundingRect(contour)
echo                 cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
echo.
echo             "# Display info"
echo             cv2.putText(frame, f"Status: {status}", (10, 30), 
echo                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
echo.
echo             cv2.putText(frame, f"Gesture: {emoji} {gesture}", (10, 60), 
echo                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
echo.
echo             cv2.putText(frame, "Controls: Palm=Play/Pause, Point=Next, Hand=Prev", (10, 90), 
echo                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
echo.
echo             cv2.putText(frame, "Press 'C' to recapture background, 'Q' to quit", (10, 420), 
echo                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
echo.
echo             "# Show camera window"
echo             cv2.imshow('🎵 Simple Gesture Control - Show Your Hand!', frame)
echo.
echo             "# Handle key presses"
echo             key = cv2.waitKey(1) & 0xFF
echo             if key == ord('q'):
echo                 break
echo             elif key == ord('c'):
echo                 hand_detector.bg_captured = False
echo                 print("🔄 Background recaptured!")
echo.
echo     except KeyboardInterrupt:
echo         print("\n🛑 Stopping...")
echo.
echo     finally:
echo         cap.release()
echo         cv2.destroyAllWindows()
echo         print("🎵 Gesture control stopped")
echo         print("✅ Spotify remains open - enjoy your music!")

echo if __name__ == "__main__":
echo     main()
) > simple_gesture_spotify.py

echo.
echo ✅ File created: simple_gesture_spotify.py
echo.