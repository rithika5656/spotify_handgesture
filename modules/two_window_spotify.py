"""
🎵 TWO-WINDOW SPOTIFY GESTURE CONTROL
Left: Spotify App | Right: Camera with Hand Gestures
"""

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import subprocess
import psutil
import os
import threading

print("🎵 Starting Two-Window Spotify Gesture Control...")

# ================================
# 🎵 SPOTIFY LAUNCHER
# ================================

def launch_spotify():
    """Launch Spotify in a separate window"""
    print("🚀 Launching Spotify...")
    
    try:
        # Try multiple ways to open Spotify
        spotify_paths = [
            r"C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe".format(os.getenv('USERNAME')),
            r"C:\Program Files\Spotify\Spotify.exe",
            "spotify"  # Command line
        ]
        
        for path in spotify_paths:
            try:
                subprocess.Popen(path, shell=True)
                print(f"✅ Spotify launched from: {path}")
                break
            except:
                continue
        else:
            # Final fallback
            os.system("start spotify:")
            print("✅ Spotify launched via system command")
        
        # Wait for Spotify to load
        time.sleep(5)
        
        # Position Spotify window on the LEFT side
        try:
            pyautogui.hotkey('win', 'left')  # Snap to left half (Windows)
            print("📐 Spotify window positioned on LEFT")
        except:
            print("⚠️  Could not auto-position Spotify window")
        
        return True
        
    except Exception as e:
        print(f"❌ Error launching Spotify: {e}")
        return False

def is_spotify_running():
    """Check if Spotify is running"""
    try:
        for proc in psutil.process_iter(['name']):
            if 'spotify' in proc.info['name'].lower():
                return True
        return False
    except:
        return False

# ================================
# ✋ SIMPLE GESTURE DETECTION
# ================================

class SimpleGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def count_fingers(self, landmarks):
        """Count extended fingers using simple rules"""
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        finger_pips = [2, 6, 10, 14, 18]  # Corresponding PIP joints
        
        extended_count = 0
        
        # Thumb (special case)
        if landmarks[4].x > landmarks[3].x:  # Thumb extended to right
            extended_count += 1
        
        # Other fingers
        for tip, pip in zip(finger_tips[1:], finger_pips[1:]):
            if landmarks[tip].y < landmarks[pip].y:  # Finger extended upward
                extended_count += 1
        
        return extended_count
    
    def detect_gesture(self, landmarks):
        """Detect gesture based on finger count"""
        finger_count = self.count_fingers(landmarks)
        
        if finger_count == 5:
            return "palm", "🖐️"
        elif finger_count == 0:
            return "fist", "✊"
        elif finger_count == 1:
            return "point", "☝️"
        elif finger_count == 2:
            return "peace", "✌️"
        elif finger_count == 3:
            return "three", "🤟"
        else:
            return f"fingers_{finger_count}", f"#{finger_count}"
    
    def process_frame(self, frame):
        """Process frame and return gesture info"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        gesture = "waiting..."
        emoji = "👋"
        landmarks_detected = False
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2)
                )
                
                # Detect gesture
                gesture, emoji = self.detect_gesture(hand_landmarks.landmark)
                landmarks_detected = True
        
        return frame, gesture, emoji, landmarks_detected

# ================================
# 🎮 GESTURE CONTROLS
# ================================

class GestureController:
    def __init__(self):
        self.last_action_time = 0
        self.action_cooldown = 1.5  # Prevent spam
        self.last_gesture = None
    
    def execute_gesture(self, gesture):
        """Execute Spotify control based on gesture"""
        current_time = time.time()
        
        # Cooldown check
        if current_time - self.last_action_time < self.action_cooldown:
            return False
        
        # Don't repeat same gesture immediately
        if gesture == self.last_gesture:
            return False
        
        self.last_gesture = gesture
        self.last_action_time = current_time
        
        # Gesture to action mapping
        actions = {
            "palm": self.play_pause,
            "fist": self.play_pause,
            "point": self.next_track,
            "peace": self.previous_track,
            "three": self.volume_up,
            "fingers_4": self.volume_down
        }
        
        action_func = actions.get(gesture)
        if action_func:
            action_func()
            return True
        
        return False
    
    def play_pause(self):
        pyautogui.press('space')
        print("🎵 Play/Pause")
    
    def next_track(self):
        pyautogui.hotkey('ctrl', 'right')
        print("⏭️ Next Track")
    
    def previous_track(self):
        pyautogui.hotkey('ctrl', 'left')
        print("⏮️ Previous Track")
    
    def volume_up(self):
        pyautogui.press('volumeup')
        print("🔊 Volume Up")
    
    def volume_down(self):
        pyautogui.press('volumedown')
        print("🔉 Volume Down")

# ================================
# 🚀 MAIN APPLICATION
# ================================

def main():
    print("🎵 TWO-WINDOW SPOTIFY GESTURE CONTROL")
    print("======================================")
    
    # Step 1: Launch or check Spotify
    if not is_spotify_running():
        print("📋 Step 1: Launching Spotify...")
        if not launch_spotify():
            print("❌ Please open Spotify MANUALLY and play some music")
            print("   Then press Enter to continue...")
            input()
    else:
        print("✅ Spotify is already running!")
    
    # Step 2: Initialize camera and gesture detection
    print("📋 Step 2: Starting camera...")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("❌ Cannot open camera!")
        return
    
    gesture_detector = SimpleGestureDetector()
    gesture_controller = GestureController()
    
    print("📋 Step 3: Starting gesture control...")
    print("\n🎮 GESTURE CONTROLS:")
    print("🖐️  OPEN PALM (5 fingers) → Play/Pause")
    print("✊  FIST (0 fingers) → Play/Pause") 
    print("☝️  POINT (1 finger) → Next Track")
    print("✌️  PEACE (2 fingers) → Previous Track")
    print("🤟 THREE (3 fingers) → Volume Up")
    print("4 FINGERS → Volume Down")
    print("\nPress 'Q' in camera window to quit")
    print("=" * 50)
    
    # Camera window setup
    cv2.namedWindow('🎵 Gesture Control - Show Your Hand!', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('🎵 Gesture Control - Show Your Hand!', 640, 480)
    
    # Position camera window on RIGHT side (you may need to drag it)
    print("💡 TIP: Drag this camera window to the RIGHT side of your screen")
    print("💡 TIP: Keep Spotify on the LEFT side")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Camera error")
                break
            
            # Mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect gestures
            processed_frame, gesture, emoji, hand_detected = gesture_detector.process_frame(frame)
            
            # Execute gesture action
            if hand_detected:
                gesture_controller.execute_gesture(gesture)
            
            # Display info on camera window
            status_text = f"Gesture: {emoji} {gesture}"
            cv2.putText(processed_frame, status_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.putText(processed_frame, "Show hand to control Spotify", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.putText(processed_frame, "Press 'Q' to quit", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show camera window
            cv2.imshow('🎵 Gesture Control - Show Your Hand!', processed_frame)
            
            # Exit on 'Q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("🎵 Gesture control stopped")
        print("✅ Spotify remains open - you can continue listening!")

if __name__ == "__main__":
    main()