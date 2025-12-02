"""
MODULE 2: Feature Extraction from Hand Landmarks
Extracts meaningful features like distances, angles, and finger states
"""

import numpy as np
from math import sqrt, atan2, degrees

class FeatureExtractor:
    """
    Extract features from 21 hand landmarks
    Features: distances between points, angles, finger states
    """
    
    # Landmark indices for reference
    WRIST = 0
    THUMB_TIP = 4
    INDEX_TIP = 8
    MIDDLE_TIP = 12
    RING_TIP = 16
    PINKY_TIP = 20
    
    THUMB_IP = 3
    INDEX_PIP = 6
    MIDDLE_PIP = 10
    RING_PIP = 14
    PINKY_PIP = 18
    
    def __init__(self):
        self.landmarks = None
    
    def distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return sqrt((point1[0] - point2[0])**2 + 
                   (point1[1] - point2[1])**2 + 
                   (point1[2] - point2[2])**2)
    
    def angle_between_points(self, p1, p2, p3):
        """
        Calculate angle at p2 formed by p1-p2-p3
        
        Args:
            p1, p2, p3: 3D points (x, y, z)
            
        Returns:
            Angle in degrees
        """
        v1 = [p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2]]
        v2 = [p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2]]
        
        dot_product = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
        
        mag1 = sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2)
        mag2 = sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        cos_angle = dot_product / (mag1 * mag2)
        cos_angle = np.clip(cos_angle, -1, 1)
        
        angle = degrees(np.arccos(cos_angle))
        return angle
    
    def is_finger_open(self, tip_idx, pip_idx):
        """
        Check if finger is open (tip above PIP joint)
        
        Args:
            tip_idx: Index of finger tip
            pip_idx: Index of PIP joint
            
        Returns:
            True if finger is open, False otherwise
        """
        if tip_idx >= len(self.landmarks) or pip_idx >= len(self.landmarks):
            return False
        return self.landmarks[tip_idx][1] < self.landmarks[pip_idx][1]
    
    def extract_features(self, landmarks):
        """
        Extract all features from hand landmarks
        
        Args:
            landmarks: Array of 21 (x, y, z) points
            
        Returns:
            Feature vector (numpy array)
        """
        self.landmarks = landmarks
        features = []
        
        # 1. Thumb-Index Pinch Distance (for Play/Pause detection)
        thumb_index_dist = self.distance(
            landmarks[self.THUMB_TIP],
            landmarks[self.INDEX_TIP]
        )
        features.append(thumb_index_dist)
        
        # 2. Thumb-Middle Pinch Distance
        thumb_middle_dist = self.distance(
            landmarks[self.THUMB_TIP],
            landmarks[self.MIDDLE_TIP]
        )
        features.append(thumb_middle_dist)
        
        # 3. All fingers open distance (Palm detection)
        palm_openness = self.distance(
            landmarks[self.INDEX_TIP],
            landmarks[self.PINKY_TIP]
        )
        features.append(palm_openness)
        
        # 4. Number of fingers open
        fingers_open = 0
        fingers_open += 1 if self.is_finger_open(self.THUMB_TIP, self.THUMB_IP) else 0
        fingers_open += 1 if self.is_finger_open(self.INDEX_TIP, self.INDEX_PIP) else 0
        fingers_open += 1 if self.is_finger_open(self.MIDDLE_TIP, self.MIDDLE_PIP) else 0
        fingers_open += 1 if self.is_finger_open(self.RING_TIP, self.RING_PIP) else 0
        fingers_open += 1 if self.is_finger_open(self.PINKY_TIP, self.PINKY_PIP) else 0
        features.append(fingers_open)
        
        # 5. Hand movement (wrist position - used for swipe detection)
        wrist_x = landmarks[self.WRIST][0]
        wrist_y = landmarks[self.WRIST][1]
        features.append(wrist_x)
        features.append(wrist_y)
        
        # 6. Angle between thumb and index
        angle_thumb_index = self.angle_between_points(
            landmarks[self.THUMB_IP],
            landmarks[self.THUMB_TIP],
            landmarks[self.INDEX_TIP]
        )
        features.append(angle_thumb_index)
        
        # 7. Angle between index and middle
        angle_index_middle = self.angle_between_points(
            landmarks[self.INDEX_TIP],
            landmarks[self.MIDDLE_TIP],
            landmarks[self.RING_TIP]
        )
        features.append(angle_index_middle)
        
        # 8. Distance from wrist to index tip (hand size)
        hand_size = self.distance(
            landmarks[self.WRIST],
            landmarks[self.INDEX_TIP]
        )
        features.append(hand_size)
        
        return np.array(features, dtype=np.float32)
    
    def extract_all_distances(self, landmarks):
        """
        Extract ALL pairwise distances between key points
        Useful for more complex ML models
        
        Args:
            landmarks: Array of 21 (x, y, z) points
            
        Returns:
            Feature vector with all distances
        """
        self.landmarks = landmarks
        features = []
        
        # Key points to compare
        key_points = [
            self.WRIST, self.THUMB_TIP, self.INDEX_TIP, 
            self.MIDDLE_TIP, self.RING_TIP, self.PINKY_TIP
        ]
        
        # Get all pairwise distances
        for i in range(len(key_points)):
            for j in range(i+1, len(key_points)):
                dist = self.distance(
                    landmarks[key_points[i]],
                    landmarks[key_points[j]]
                )
                features.append(dist)
        
        return np.array(features, dtype=np.float32)
