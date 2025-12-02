"""
MODULE 6: REAL-TIME INTEGRATION
Main pipeline combining all modules
"""

import cv2
import numpy as np
import time
import os
from modules.hand_detection import HandDetector
from modules.feature_extraction import FeatureExtractor
from modules.gesture_classifier import GestureClassifier
from modules.action_mapper import ActionMapper
from modules.media_controller import MediaController

class GestureControlPipeline:
    """
    Main pipeline for real-time gesture detection and media control
    """
    
    def __init__(self, model_path="data/gesture_model_random_forest", confidence_threshold=0.6):
        """
        Initialize gesture control pipeline
        
        Args:
            model_path: Path to trained gesture model
            confidence_threshold: Minimum confidence for gesture detection
        """
        print("🚀 Initializing Gesture Control Pipeline...")
        
        # Initialize components
        self.hand_detector = HandDetector(max_hands=1)
        self.feature_extractor = FeatureExtractor()
        self.gesture_classifier = GestureClassifier(model_type='random_forest')
        self.action_mapper = ActionMapper()
        self.media_controller = MediaController()
        
        # Load pre-trained model
        self.confidence_threshold = confidence_threshold
        if os.path.exists(f"{model_path}.pkl"):
            print(f"📦 Loading trained model from {model_path}...")
            self.gesture_classifier.load_model(model_path)
        else:
            print(f"⚠️  Model not found at {model_path}")
            print("Please train a model first using train_model.py")
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        # Gesture history for smoothing
        self.gesture_history = []
        self.gesture_history_size = 5
        self.last_gesture = None
        self.gesture_confidence = 0.0
        
        # Performance monitoring
        self.frame_count = 0
        self.start_time = time.time()
        
        print("✓ Pipeline initialized successfully!\n")
    
    def process_frame(self, frame):
        """
        Process a single frame
        
        Args:
            frame: Input frame from camera
            
        Returns:
            frame: Processed frame with visualizations
            gesture: Detected gesture class
            confidence: Confidence score
        """
        # Detect hands
        frame, landmarks_list = self.hand_detector.detect_hands(frame)
        
        gesture = None
        confidence = 0.0
        action = None
        
        if len(landmarks_list) > 0:
            # Extract features from detected hand
            landmarks = landmarks_list[0]
            features = self.feature_extractor.extract_features(landmarks)
            
            # Predict gesture
            gesture, confidence = self.gesture_classifier.predict(features)
            
            # Only use prediction if confidence is high enough
            if confidence >= self.confidence_threshold:
                # Smooth gesture detection using history
                self.gesture_history.append(gesture)
                if len(self.gesture_history) > self.gesture_history_size:
                    self.gesture_history.pop(0)
                
                # Use majority gesture from history
                gesture = max(set(self.gesture_history), key=self.gesture_history.count)
                
                # Get action for gesture
                action = self.action_mapper.get_action(gesture)
                
                # Execute media control
                if action and gesture != self.last_gesture:
                    self.media_controller.execute_action(action)
                    self.last_gesture = gesture
            else:
                gesture = None
                action = None
        
        # Draw visualizations
        frame = self._draw_ui(frame, gesture, confidence, action)
        
        return frame, gesture, confidence
    
    def _draw_ui(self, frame, gesture, confidence, action):
        """
        Draw UI on frame
        
        Args:
            frame: Input frame
            gesture: Detected gesture class
            confidence: Confidence score
            action: Mapped action
            
        Returns:
            Frame with UI drawn
        """
        h, w, _ = frame.shape
        
        # Draw semi-transparent background for info panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (400, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Gesture information
        gesture_text = "Gesture: "
        if gesture is not None:
            gesture_name = self.gesture_classifier.get_gesture_name(gesture)
            gesture_text += gesture_name
            color = (0, 255, 0)
        else:
            gesture_text += "No hand detected"
            color = (0, 165, 255)
        
        cv2.putText(
            frame, gesture_text,
            (10, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, color, 2
        )
        
        # Confidence
        confidence_text = f"Confidence: {confidence:.2%}"
        confidence_color = (0, 255, 0) if confidence >= self.confidence_threshold else (0, 0, 255)
        cv2.putText(
            frame, confidence_text,
            (10, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8, confidence_color, 2
        )
        
        # Action
        if action:
            action_desc = ActionMapper.get_action_description(action)
            cv2.putText(
                frame, action_desc,
                (10, 115),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255, 165, 0), 2
            )
        
        # Volume indicator
        try:
            volume = self.media_controller.get_volume()
            volume_bar_width = int(volume * 100)
            cv2.rectangle(frame, (w-150, 10), (w-10, 40), (200, 200, 200), 2)
            cv2.rectangle(frame, (w-150, 10), (w-150+volume_bar_width, 40), (0, 255, 0), -1)
            cv2.putText(
                frame, f"Vol: {volume:.0%}",
                (w-140, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 1
            )
        except:
            pass
        
        # FPS
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
        
        cv2.putText(
            frame, f"FPS: {fps:.1f}",
            (10, h-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (255, 255, 0), 1
        )
        
        # Instructions
        cv2.putText(
            frame, "Q: Quit | S: Settings",
            (w-250, h-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 1
        )
        
        return frame
    
    def run(self, camera_id=0):
        """
        Run real-time gesture control
        
        Args:
            camera_id: Camera device ID (usually 0)
        """
        cap = cv2.VideoCapture(camera_id)
        
        print("\n" + "="*60)
        print("🎥 REAL-TIME GESTURE CONTROL STARTED")
        print("="*60)
        print("Controls:")
        print("  Q - Quit")
        print("  S - Show/Hide Settings")
        print("="*60 + "\n")
        
        show_settings = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read from camera")
                break
            
            # Flip frame horizontally for selfie view
            frame = cv2.flip(frame, 1)
            
            # Process frame
            frame, gesture, confidence = self.process_frame(frame)
            
            # Show settings if requested
            if show_settings:
                frame = self._draw_settings(frame)
            
            # Display frame
            cv2.imshow("Gesture Control - Media Player", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n✓ Exiting gesture control...")
                break
            elif key == ord('s'):
                show_settings = not show_settings
        
        cap.release()
        cv2.destroyAllWindows()
        
        print("✓ Gesture control stopped.\n")
    
    def _draw_settings(self, frame):
        """Draw settings panel on frame"""
        h, w, _ = frame.shape
        
        # Draw semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (w-250, 50), (w-10, 200), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        
        # Settings text
        settings = [
            f"Threshold: {self.confidence_threshold:.2f}",
            f"Gesture History: {self.gesture_history_size}",
            f"Detected Gestures: {len(self.gesture_classifier.GESTURES)}"
        ]
        
        for i, setting in enumerate(settings):
            cv2.putText(
                frame, setting,
                (w-240, 80 + i*40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 255), 1
            )
        
        return frame

if __name__ == "__main__":
    # Initialize and run pipeline
    try:
        pipeline = GestureControlPipeline(
            model_path="data/gesture_model_random_forest",
            confidence_threshold=0.6
        )
        pipeline.run()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease train a model first:")
        print("  python train_model.py")
