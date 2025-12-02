"""
🎵 COMPLETE GESTURE-CONTROLLED SPOTIFY
Hand Gesture Recognition + Spotify Control
"""

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import subprocess
import psutil
import os
import json
from sklearn.ensemble import RandomForestClassifier
import joblib

# ================================
# 🎵 SPOTIFY CONTROLLER
# ================================

class SpotifyController:
    def __init__(self):
        self.last_action_time = 0
        self.action_cooldown = 0.5
        
    def is_spotify_running(self):
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if 'spotify' in proc.info['name'].lower():
                    return True
            return False
        except:
            return False
    
    def launch_spotify(self):
        try:
            print("🚀 Launching Spotify...")
            # Try multiple ways to open Spotify
            try:
                subprocess.Popen([r"C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe".format(os.getenv('USERNAME'))])
            except:
                try:
                    subprocess.Popen(["C:\\Program Files\\Spotify\\Spotify.exe"])
                except:
                    os.system("start spotify:")
            
            time.sleep(5)  # Wait for Spotify to load
            return True
        except Exception as e:
            print(f"❌ Error launching Spotify: {e}")
            return False
    
    def _check_cooldown(self):
        current_time = time.time()
        return (current_time - self.last_action_time) >= self.action_cooldown
    
    def play_pause(self):
        if self._check_cooldown():
            pyautogui.press('space')
            self.last_action_time = time.time()
            print("▶️ Play/Pause")
            return True
        return False
    
    def next_track(self):
        if self._check_cooldown():
            pyautogui.hotkey('ctrl', 'right')
            self.last_action_time = time.time()
            print("⏭️ Next Track")
            return True
        return False
    
    def previous_track(self):
        if self._check_cooldown():
            pyautogui.hotkey('ctrl', 'left')
            self.last_action_time = time.time()
            print("⏮️ Previous Track")
            return True
        return False
    
    def volume_up(self):
        if self._check_cooldown():
            pyautogui.press('volumeup')
            self.last_action_time = time.time()
            print("🔊 Volume Up")
            return True
        return False
    
    def volume_down(self):
        if self._check_cooldown():
            pyautogui.press('volumedown')
            self.last_action_time = time.time()
            print("🔉 Volume Down")
            return True
        return False

# ================================
# ✋ HAND GESTURE DETECTOR
# ================================

class HandGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Load trained model
        try:
            self.model = joblib.load('data/gesture_model_random_forest')
            print("✅ Gesture model loaded successfully")
        except:
            print("❌ No trained model found. Using default gestures.")
            self.model = None
    
    def extract_features(self, landmarks):
        """Extract hand gesture features from landmarks"""
        features = []
        
        # Thumb to index distance
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        thumb_index_dist = np.sqrt(
            (thumb_tip.x - index_tip.x)**2 + 
            (thumb_tip.y - index_tip.y)**2
        )
        features.append(thumb_index_dist)
        
        # Number of extended fingers
        extended_fingers = self.count_extended_fingers(landmarks)
        features.append(extended_fingers)
        
        # Hand openness (average distance from wrist to fingertips)
        wrist = landmarks[0]
        fingertip_distances = []
        for tip_idx in [4, 8, 12, 16, 20]:  # All fingertips
            dist = np.sqrt(
                (wrist.x - landmarks[tip_idx].x)**2 + 
                (wrist.y - landmarks[tip_idx].y)**2
            )
            fingertip_distances.append(dist)
        features.append(np.mean(fingertip_distances))
        
        return features
    
    def count_extended_fingers(self, landmarks):
        """Count how many fingers are extended"""
        extended_count = 0
        
        # Thumb (different logic)
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        if thumb_tip.x > thumb_ip.x:  # Right hand thumb extended
            extended_count += 1
        
        # Other fingers
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        finger_pips = [6, 10, 14, 18]  # PIP joints
        
        for tip_idx, pip_idx in zip(finger_tips, finger_pips):
            if landmarks[tip_idx].y < landmarks[pip_idx].y:  # Finger extended
                extended_count += 1
        
        return extended_count
    
    def predict_gesture(self, features):
        """Predict gesture from features"""
        if self.model is None:
            # Fallback: use rule-based detection
            extended_fingers = int(features[1])
            thumb_index_dist = features[0]
            
            if extended_fingers == 5:
                return "palm"
            elif extended_fingers == 0:
                return "fist"
            elif thumb_index_dist < 0.05:
                return "pinch"
            elif extended_fingers == 1:
                return "point"
            elif extended_fingers == 2:
                return "v_sign"
            else:
                return "unknown"
        else:
            # Use trained model
            prediction = self.model.predict([features])[0]
            return prediction
    
    def process_frame(self, frame):
        """Process frame and detect gestures"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        gesture = "none"
        features = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                
                # Extract features and predict gesture
                features = self.extract_features(hand_landmarks.landmark)
                gesture = self.predict_gesture(features)
                
                # Display gesture text
                cv2.putText(frame, f'Gesture: {gesture}', (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return frame, gesture, features

# ================================
# 🎮 GESTURE TO ACTION MAPPER
# ================================

class GestureActionMapper:
    def __init__(self, spotify_controller):
        self.spotify_ctrl = spotify_controller
        self.last_gesture = None
        self.gesture_cooldown = 1.0  # Prevent rapid gesture changes
    
    def map_to_action(self, gesture):
        """Map detected gesture to Spotify action"""
        current_time = time.time()
        
        # Prevent rapid gesture changes
        if (self.last_gesture == gesture and 
            current_time - getattr(self, 'last_action_time', 0) < self.gesture_cooldown):
            return None
        
        self.last_gesture = gesture
        self.last_action_time = current_time
        
        # Gesture to action mapping
        action_map = {
            'palm': 'play_pause',
            'fist': 'play_pause',
            'point': 'next_track',
            'v_sign': 'previous_track',
            'pinch': 'volume_up'
        }
        
        return action_map.get(gesture)
    
    def execute_action(self, gesture):
        """Execute the corresponding Spotify action"""
        action = self.map_to_action(gesture)
        
        if action:
            print(f"🎯 Gesture: {gesture} -> Action: {action}")
            
            if action == 'play_pause':
                self.spotify_ctrl.play_pause()
            elif action == 'next_track':
                self.spotify_ctrl.next_track()
            elif action == 'previous_track':
                self.spotify_ctrl.previous_track()
            elif action == 'volume_up':
                self.spotify_ctrl.volume_up()
            elif action == 'volume_down':
                self.spotify_ctrl.volume_down()
            
            return True
        return False

# ================================
# 🚀 MAIN APPLICATION
# ================================

def main():
    print("🎵 Starting Gesture-Controlled Spotify...")
    
    # Initialize components
    spotify_ctrl = SpotifyController()
    gesture_detector = HandGestureDetector()
    action_mapper = GestureActionMapper(spotify_ctrl)
    
    # Auto-launch Spotify
    print("🎵 Checking Spotify...")
    if not spotify_ctrl.is_spotify_running():
        print("🚀 Launching Spotify automatically...")
        if not spotify_ctrl.launch_spotify():
            print("❌ Could not launch Spotify automatically")
            print("📋 Please open Spotify manually and play some music")
    else:
        print("✅ Spotify is running!")
    
    # Wait a moment for Spotify to load
    time.sleep(2)
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("❌ Cannot open camera")
        return
    
    print("📷 Camera started - Show your hand gestures!")
    print("\n🎮 GESTURE CONTROLS:")
    print("✋ PALM → Play/Pause")
    print("✊ FIST → Play/Pause") 
    print("👉 POINT → Next Track")
    print("✌️ V_SIGN → Previous Track")
    print("🤏 PINCH → Volume Up")
    print("\nPress 'Q' to quit")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Cannot read frame from camera")
                break
            
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process frame and detect gestures
            processed_frame, gesture, features = gesture_detector.process_frame(frame)
            
            # Execute Spotify action if gesture detected
            if gesture != "none":
                action_mapper.execute_action(gesture)
            
            # Display instructions
            cv2.putText(processed_frame, "Show hand gestures to control Spotify", 
                       (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show frame
            cv2.imshow('Gesture Controlled Spotify', processed_frame)
            
            # Exit on 'Q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n⏹️ Stopping...")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("🎵 Gesture control stopped")

if __name__ == "__main__":
    main()