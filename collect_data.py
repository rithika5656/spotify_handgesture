"""
DATA COLLECTION SCRIPT
Record hand gestures and collect training data
"""

import cv2
import os
import numpy as np
from modules.hand_detection import HandDetector
from modules.feature_extraction import FeatureExtractor
import json
import time
import argparse

class DataCollector:
    """Collect training data for gesture recognition"""
    
    GESTURES = {
        0: "PALM",       # ✋ Open hand - Volume Up
        1: "FIST",       # ✊ Closed fist - Volume Down
        2: "PINCH",      # 🤏 Thumb and index together - Play/Pause
        3: "POINT",      # 👉 Index finger pointing - Next
        4: "V_SIGN",     # ✌ Peace sign - Previous
    }
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.hand_detector = HandDetector(max_hands=1)
        self.feature_extractor = FeatureExtractor()
        
        # Create data directories
        os.makedirs(data_dir, exist_ok=True)
        for gesture_id, gesture_name in self.GESTURES.items():
            gesture_dir = os.path.join(data_dir, f"{gesture_id}_{gesture_name}")
            os.makedirs(gesture_dir, exist_ok=True)
    
    def collect_gesture_data(self, gesture_id, samples_per_gesture=50, auto=False, interval=0.5):
        """
        Collect samples for a specific gesture
        
        Args:
            gesture_id: ID of gesture to collect
            samples_per_gesture: Number of samples to collect
        """
        gesture_name = self.GESTURES[gesture_id]
        gesture_dir = os.path.join(self.data_dir, f"{gesture_id}_{gesture_name}")
        
        cap = cv2.VideoCapture(0)
        collected = 0
        
        print(f"\n{'='*60}")
        print(f"🎥 Collecting data for gesture: {gesture_name}")
        print(f"{'='*60}")
        print(f"Position your hand in the camera and press 'SPACE' to capture frames")
        print(f"Target: {samples_per_gesture} samples")
        print(f"Press 'q' to finish\n")
        
        last_capture = 0.0
        while collected < samples_per_gesture:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame, landmarks_list = self.hand_detector.detect_hands(frame)
            
            # Display instructions
            cv2.putText(
                frame,
                f"{gesture_name}: {collected}/{samples_per_gesture}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            cv2.putText(
                frame,
                "SPACE: Capture | Q: Quit",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )
            
            cv2.imshow("Data Collection", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            # Manual capture (SPACE) when hand detected
            if not auto and key == ord(' ') and len(landmarks_list) > 0:
                # Extract features from hand
                landmarks = landmarks_list[0]
                features = self.feature_extractor.extract_features(landmarks)
                
                # Save features and landmarks
                sample_id = len(os.listdir(gesture_dir))
                feature_file = os.path.join(gesture_dir, f"features_{sample_id}.npy")
                landmarks_file = os.path.join(gesture_dir, f"landmarks_{sample_id}.npy")
                
                np.save(feature_file, features)
                np.save(landmarks_file, landmarks)
                
                collected += 1
                print(f"✓ Captured sample {collected}/{samples_per_gesture}")
            # Auto capture mode: capture automatically when a hand is detected
            if auto and len(landmarks_list) > 0:
                now = time.time()
                if now - last_capture >= interval:
                    landmarks = landmarks_list[0]
                    features = self.feature_extractor.extract_features(landmarks)

                    sample_id = len(os.listdir(gesture_dir))
                    feature_file = os.path.join(gesture_dir, f"features_{sample_id}.npy")
                    landmarks_file = os.path.join(gesture_dir, f"landmarks_{sample_id}.npy")

                    np.save(feature_file, features)
                    np.save(landmarks_file, landmarks)

                    collected += 1
                    last_capture = now
                    print(f"✓ Auto-captured sample {collected}/{samples_per_gesture}")
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n✓ Completed collecting {collected} samples for {gesture_name}\n")
    
    def collect_all_gestures(self, samples_per_gesture=50):
        """
        Collect data for all gestures
        
        Args:
            samples_per_gesture: Samples to collect per gesture
        """
        print(f"\n\n{'='*60}")
        print(f"🎬 GESTURE DATA COLLECTION INTERFACE")
        print(f"{'='*60}")
        print(f"You will collect {samples_per_gesture} samples for each gesture")
        print(f"Total samples to collect: {len(self.GESTURES) * samples_per_gesture}\n")
        
        for gesture_id in sorted(self.GESTURES.keys()):
            input(f"Press ENTER to start collecting {self.GESTURES[gesture_id]}...")
            self.collect_gesture_data(gesture_id, samples_per_gesture)
        
        print(f"\n{'='*60}")
        print(f"✓ Data collection complete!")
        print(f"{'='*60}\n")
    
    def create_training_dataset(self):
        """
        Load all collected data and create training dataset
        
        Returns:
            X: Feature matrix (n_samples, n_features)
            y: Label vector (n_samples,)
        """
        X = []
        y = []
        
        for gesture_id in sorted(self.GESTURES.keys()):
            gesture_name = self.GESTURES[gesture_id]
            gesture_dir = os.path.join(self.data_dir, f"{gesture_id}_{gesture_name}")
            
            feature_files = [f for f in os.listdir(gesture_dir) if f.startswith("features_")]
            
            for feature_file in feature_files:
                feature_path = os.path.join(gesture_dir, feature_file)
                features = np.load(feature_path)
                
                X.append(features)
                y.append(gesture_id)
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"✓ Loaded dataset: {X.shape[0]} samples, {X.shape[1]} features")
        print(f"✓ Classes: {len(np.unique(y))}")
        
        return X, y

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect hand gesture data')
    parser.add_argument('--samples', type=int, default=50, help='Samples per gesture')
    parser.add_argument('--auto', action='store_true', help='Enable automatic capture when a hand is detected')
    parser.add_argument('--interval', type=float, default=0.5, help='Interval (s) between auto captures')
    args = parser.parse_args()

    collector = DataCollector()
    # If auto is requested, pass the flags through to collection
    if args.auto:
        for gesture_id in sorted(collector.GESTURES.keys()):
            input(f"Press ENTER to start auto-collecting {collector.GESTURES[gesture_id]}...")
            collector.collect_gesture_data(gesture_id, samples_per_gesture=args.samples, auto=True, interval=args.interval)
        print(f"\n{'='*60}\n✓ Auto data collection complete!\n{'='*60}\n")
    else:
        collector.collect_all_gestures(samples_per_gesture=args.samples)
