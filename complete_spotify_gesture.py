"""
🎵 SPOTIFY GESTURE CONTROL WITH HAND SKELETON
Exact MediaPipe skeleton model with 21 landmarks
"""

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import subprocess
import psutil
import os

print("🎵 Starting Spotify Gesture Control with Hand Skeleton...")

# ================================
# ✋ HAND SKELETON DETECTOR (MediaPipe)
# ================================

class HandSkeletonDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        print("✅ Hand Skeleton Detector initialized")
    
    def detect_hands(self, frame):
        """Detect hands and return landmarks with skeleton"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        landmarks_list = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw the hand skeleton (EXACTLY like your previous working version)
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2)
                )
                landmarks_list.append(hand_landmarks.landmark)
        
        return frame, landmarks_list, results.multi_hand_landmarks
    
    def count_fingers(self, landmarks):
        """Count extended fingers using landmark positions"""
        if not landmarks:
            return 0, "no_hand"
        
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        finger_pips = [2, 6, 10, 14, 18]  # PIP joints
        
        extended_count = 0
        
        # Thumb (special logic)
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        if thumb_tip.x > thumb_ip.x:  # Thumb extended
            extended_count += 1
        
        # Other four fingers
        for tip_idx, pip_idx in zip(finger_tips[1:], finger_pips[1:]):
            if landmarks[tip_idx].y < landmarks[pip_idx].y:  # Finger extended
                extended_count += 1
        
        return extended_count
    
    def detect_gesture(self, landmarks):
        """Detect specific gestures from hand landmarks"""
        if not landmarks:
            return "no_hand", "❌", 0
        
        finger_count = self.count_fingers(landmarks)
        
        # Gesture detection based on finger count
        if finger_count == 5:
            return "palm", "🖐️", finger_count
        elif finger_count == 0:
            return "fist", "✊", finger_count
        elif finger_count == 1:
            # Check which finger is extended
            if landmarks[8].y < landmarks[6].y:  # Index finger extended
                return "point", "☝️", finger_count
        elif finger_count == 2:
            # Check if it's peace sign (index + middle)
            if (landmarks[8].y < landmarks[6].y and  # Index extended
                landmarks[12].y < landmarks[10].y):  # Middle extended
                return "v_sign", "✌️", finger_count
        
        return "unknown", "❓", finger_count

# ================================
# 🎵 SPOTIFY CONTROLLER
# ================================

class SpotifyController:
    def __init__(self):
        self.last_action_time = 0
        self.action_cooldown = 2.0
        self.is_spotify_open = False
        
        print("🎵 Spotify Controller initialized")
    
    def is_spotify_running(self):
        """Check if Spotify is running"""
        try:
            for proc in psutil.process_iter(['name']):
                if 'spotify' in proc.info['name'].lower():
                    self.is_spotify_open = True
                    return True
            self.is_spotify_open = False
            return False
        except:
            return False
    
    def launch_spotify(self):
        """Launch Spotify application"""
        try:
            print("🚀 Launching Spotify...")
            os.system("start spotify:")
            time.sleep(5)
            self.is_spotify_open = True
            print("✅ Spotify launched")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _check_cooldown(self):
        """Prevent rapid actions"""
        return (time.time() - self.last_action_time) >= self.action_cooldown
    
    def execute_action(self, gesture):
        """Execute action based on gesture"""
        if not self._check_cooldown():
            return False
        
        try:
            if gesture == "palm":
                pyautogui.press('space')
                print("▶️ Play/Pause")
            elif gesture == "fist":
                pyautogui.press('volumedown')
                print("🔉 Volume Down")
            elif gesture == "point":
                pyautogui.hotkey('ctrl', 'right')
                print("⏭️ Next Track")
            elif gesture == "v_sign":
                pyautogui.hotkey('ctrl', 'left')
                print("⏮️ Previous Track")
            
            self.last_action_time = time.time()
            return True
        except Exception as e:
            print(f"❌ Action error: {e}")
            return False

# ================================
# 🚀 MAIN APPLICATION
# ================================

class SpotifyGestureControl:
    def __init__(self):
        print("🎵 Initializing Spotify Gesture Control with Hand Skeleton...")
        
        # Initialize components
        self.hand_detector = HandSkeletonDetector()
        self.spotify_controller = SpotifyController()
        
        # Gesture tracking
        self.last_gesture = None
        
        # Check Spotify
        print("\n🔍 Checking Spotify...")
        if not self.spotify_controller.is_spotify_running():
            print("⚠️  Spotify not running")
            if input("Launch Spotify automatically? (y/n): ").lower() == 'y':
                self.spotify_controller.launch_spotify()
            else:
                print("📋 Please open Spotify manually and play music")
        else:
            print("✅ Spotify is running!")
        
        print("✓ Hand Skeleton control ready!\n")
    
    def process_frame(self, frame):
        """Process frame and detect gestures with skeleton"""
        # Detect hands with skeleton
        frame, landmarks_list, hand_landmarks = self.hand_detector.detect_hands(frame)
        
        gesture = "no_hand"
        emoji = "❌"
        finger_count = 0
        
        if landmarks_list:
            # Get gesture from landmarks
            gesture, emoji, finger_count = self.hand_detector.detect_gesture(landmarks_list[0])
            
            # Execute action if new gesture detected
            if gesture != "no_hand" and gesture != self.last_gesture:
                print(f"🎯 Skeleton Detected: {emoji} {gesture} ({finger_count} fingers)")
                self.spotify_controller.execute_action(gesture)
                self.last_gesture = gesture
        
        # Draw UI
        frame = self._draw_ui(frame, gesture, emoji, finger_count)
        
        return frame, gesture
    
    def _draw_ui(self, frame, gesture, emoji, finger_count):
        """Draw user interface"""
        h, w = frame.shape[:2]
        
        # Info panel background
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Title
        cv2.putText(frame, "🎵 SPOTIFY SKELETON CONTROL", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Gesture info
        gesture_color = (0, 255, 0) if gesture != "no_hand" else (0, 165, 255)
        cv2.putText(frame, f"Gesture: {emoji} {gesture}", (10, 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, gesture_color, 2)
        
        # Finger count
        if gesture != "no_hand":
            cv2.putText(frame, f"Fingers: {finger_count}", (10, 95), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Instructions
        cv2.putText(frame, "Press 'Q' to quit", (10, h-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        return frame
    
    def run(self):
        """Main application loop"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if not cap.isOpened():
            print("❌ Cannot open camera")
            return
        
        print("\n" + "="*50)
        print("🎵 SPOTIFY HAND SKELETON CONTROL STARTED")
        print("="*50)
        print("GESTURE MAPPING:")
        print("🖐️ Open Hand (5 fingers) → Play/Pause")
        print("✊ Closed Fist (0 fingers) → Volume Down") 
        print("☝️ Pointing (1 finger) → Next Track")
        print("✌️ Peace Sign (2 fingers) → Previous Track")
        print("="*50)
        print("Press 'Q' to quit")
        print("="*50)
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Camera error")
                    break
                
                # Mirror the frame
                frame = cv2.flip(frame, 1)
                
                # Process frame with skeleton detection
                frame, gesture = self.process_frame(frame)
                
                # Show frame
                cv2.imshow("🎵 Spotify Hand Skeleton", frame)
                
                # Handle keys
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                
        except KeyboardInterrupt:
            print("\n⏹️ Stopping...")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("🎵 Hand skeleton control stopped")

# ================================
# 🚀 START THE PROGRAM
# ================================

if __name__ == "__main__":
    try:
        # Create and run the application
        app = SpotifyGestureControl()
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📋 To fix MediaPipe installation:")
        print("1. Use Python 3.11 (not 3.14)")
        print("2. Run: pip install mediapipe opencv-python numpy pyautogui psutil")
        print("3. Or try: pip install mediapipe --user")