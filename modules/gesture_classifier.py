"""
MODULE 3: Gesture Classification
Train and use ML models to classify hand gestures
"""

import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import os

class GestureClassifier:
    """
    Train and predict hand gestures using ML models
    Supports SVM, Random Forest, and Neural Network
    """
    
    # Gesture classes
    GESTURES = {
        0: "PALM",           # ✋ Open palm - Volume Up
        1: "FIST",           # ✊ Closed fist - Volume Down
        2: "PINCH",          # 🤏 Thumb-Index pinch - Play/Pause
        3: "POINT",          # 👉 Index finger pointing - Swipe Right
        4: "V_SIGN",         # ✌ Peace sign - Swipe Left
    }
    
    GESTURE_NAMES = {v: k for k, v in GESTURES.items()}
    
    def __init__(self, model_type='random_forest'):
        """
        Initialize gesture classifier
        
        Args:
            model_type: 'svm', 'random_forest', or 'neural_network'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Initialize model
        if model_type == 'svm':
            self.model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        elif model_type == 'neural_network':
            self.model = MLPClassifier(
                hidden_layer_sizes=(128, 64, 32),
                max_iter=1000,
                random_state=42,
                early_stopping=True,
                validation_fraction=0.1
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def train(self, X_train, y_train):
        """
        Train the gesture classifier
        
        Args:
            X_train: Training features (n_samples, n_features)
            y_train: Training labels (n_samples,)
        """
        print(f"Training {self.model_type} model...")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        # Get accuracy on training set
        accuracy = self.model.score(X_train_scaled, y_train)
        print(f"Training accuracy: {accuracy:.2%}")
    
    def predict(self, features):
        """
        Predict gesture from features
        
        Args:
            features: Feature vector (n_features,)
            
        Returns:
            Tuple of (gesture_class, confidence)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Scale features
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        
        # Get confidence
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(features_scaled)[0]
            confidence = probabilities[prediction]
        else:
            confidence = 0.0
        
        return prediction, confidence
    
    def predict_batch(self, X):
        """
        Predict multiple samples
        
        Args:
            X: Feature matrix (n_samples, n_features)
            
        Returns:
            predictions: Array of gesture classes
            confidences: Array of confidence scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(X_scaled)
            confidences = np.max(probabilities, axis=1)
        else:
            confidences = np.ones(len(predictions))
        
        return predictions, confidences
    
    def save_model(self, model_path):
        """
        Save trained model to disk
        
        Args:
            model_path: Path to save model
        """
        if not self.is_trained:
            print("Warning: Model not trained yet!")
        
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save model and scaler
        joblib.dump(self.model, f"{model_path}.pkl")
        joblib.dump(self.scaler, f"{model_path}_scaler.pkl")
        
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path):
        """
        Load trained model from disk
        
        Args:
            model_path: Path to load model
        """
        self.model = joblib.load(f"{model_path}.pkl")
        self.scaler = joblib.load(f"{model_path}_scaler.pkl")
        self.is_trained = True
        
        print(f"Model loaded from {model_path}")
    
    def get_gesture_name(self, gesture_class):
        """
        Get gesture name from class
        
        Args:
            gesture_class: Gesture class index
            
        Returns:
            Gesture name string
        """
        return self.GESTURES.get(gesture_class, "UNKNOWN")
