print("🎵 SIMPLE GESTURE SPOTIFY CONTROL")
print("No MediaPipe - Using OpenCV Only")

import cv2
import numpy as np
import pyautogui
import time
import subprocess
import psutil
import os

def launch_spotify():
    print("🚀 Launching Spotify...")
    try:
        os.system("start spotify:")
        time.sleep(5)
        return True
    except:
        return False

def is_spotify_running():
    try:
        for proc in psutil.process_iter(['name']):
            if 'spotify' in proc.info['name'].lower():
                return True
        return False
    except:
        return False

class SimpleHandDetector:
    def __init__(self):
        self.background = None
        self.bg_captured = False
        
    def capture_background(self, frame):
        self.background = cv2.GaussianBlur(frame, (21, 21), 0)
        self.bg_captured = True
        print("✅ Background captured")
    
    def detect_hand_contour(self, frame):
        if not self.bg_captured:
            self.capture_background(frame)
            return None, "Capturing background..."
        
        blurred = cv2.GaussianBlur(frame, (21, 21), 0)
        diff = cv2.absdiff(self.background, blurred)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
        
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, "No hand"
        
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        if area < 1000:
            return None, "Hand small"
        
        return largest_contour, "Hand OK"
    
    def detect_gesture(self, contour):
        if contour is None:
            return "no_hand", "❌"
        
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        contour_area = cv2.contourArea(contour)
        solidity = float(contour_area) / hull_area if hull_area > 0 else 0
        
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        
        if solidity > 0.9:
            return "fist", "✊"
        elif aspect_ratio > 1.2:
            return "palm", "🖐️"
        elif aspect_ratio < 0.8:
            return "point", "☝️"
        else:
            return "hand", "👋"

class GestureController:
    def __init__(self):
        self.last_action_time = 0
        self.cooldown = 2.0
    
    def execute_gesture(self, gesture):
        current_time = time.time()
        if current_time - self.last_action_time < self.cooldown:
            return False
        
        self.last_action_time = current_time
        
        if gesture == "palm" or gesture == "fist":
            pyautogui.press('space')
            print("🎵 Play/Pause")
        elif gesture == "point":
            pyautogui.hotkey('ctrl', 'right')
            print("⏭️ Next")
        elif gesture == "hand":
            pyautogui.hotkey('ctrl', 'left')
            print("⏮️ Previous")
        
        return True

def main():
    print("🎵 Starting...")
    
    if not is_spotify_running():
        print("Opening Spotify...")
        launch_spotify()
    else:
        print("✅ Spotify running")
    
    cap = cv2.VideoCapture(0)
    detector = SimpleHandDetector()
    controller = GestureController()
    
    print("📷 Camera started")
    print("🖐️ Show hand to control Spotify")
    print("❌ Press Q to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        contour, status = detector.detect_hand_contour(frame)
        gesture, emoji = detector.detect_gesture(contour)
        
        if gesture != "no_hand":
            controller.execute_gesture(gesture)
        
        if contour is not None:
            cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        cv2.putText(frame, f"Status: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Gesture: {emoji} {gesture}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, "Press Q to quit", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('🎵 Gesture Control', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("🎵 Stopped")

if __name__ == "__main__":
    main()