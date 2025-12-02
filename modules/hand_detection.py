"""
MODULE 1: Hand Detection using MediaPipe
Detects hands in video frames and extracts 21 landmark points
"""

import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    """
    Detects hand landmarks using MediaPipe
    Returns 21 landmark coordinates for each detected hand
    """
    
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, tracking_con=0.5):
        """
        Initialize hand detector
        
        Args:
            mode: Static image mode (False = video mode)
            max_hands: Maximum number of hands to detect
            detection_con: Minimum confidence for hand detection
            tracking_con: Minimum confidence for hand tracking
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.tracking_con = tracking_con
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.tracking_con
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def detect_hands(self, frame):
        """
        Detect hands in frame
        
        Args:
            frame: Input image frame (BGR format)
            
        Returns:
            frame: Frame with hand landmarks drawn
            landmarks: List of 21 (x, y, z) coordinates for each detected hand
        """
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        landmarks_list = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extract 21 landmarks for each hand
                hand_coords = []
                for landmark in hand_landmarks.landmark:
                    hand_coords.append([landmark.x, landmark.y, landmark.z])
                landmarks_list.append(np.array(hand_coords))
                
                # Draw hand landmarks on frame (optional visualization)
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        return frame, landmarks_list
    
    def get_hand_position(self, landmarks):
        """
        Get bounding box of hand
        
        Args:
            landmarks: 21 landmark points
            
        Returns:
            Tuple of (x_min, y_min, x_max, y_max, width, height)
        """
        if len(landmarks) == 0:
            return None
            
        x_coords = landmarks[:, 0]
        y_coords = landmarks[:, 1]
        
        x_min, x_max = x_coords.min(), x_coords.max()
        y_min, y_max = y_coords.min(), y_coords.max()
        
        width = x_max - x_min
        height = y_max - y_min
        
        return (x_min, y_min, x_max, y_max, width, height)
