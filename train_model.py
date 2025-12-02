"""
TRAINING SCRIPT
Train gesture classification model
"""

import numpy as np
from sklearn.model_selection import train_test_split
from collect_data import DataCollector
from modules.gesture_classifier import GestureClassifier
import os

def train_gesture_model(model_type='random_forest', test_size=0.2, random_state=42):
    """
    Train gesture classification model
    
    Args:
        model_type: Type of model ('svm', 'random_forest', 'neural_network')
        test_size: Fraction of data to use for testing
        random_state: Random seed for reproducibility
    """
    
    print(f"\n{'='*60}")
    print(f"🤖 GESTURE CLASSIFIER TRAINING")
    print(f"{'='*60}\n")
    
    # Check if training data exists
    collector = DataCollector()
    
    # Check if data directory has any samples
    data_samples = []
    for root, dirs, files in os.walk(collector.data_dir):
        data_samples.extend([f for f in files if f.startswith("features_")])
    
    if len(data_samples) == 0:
        print("⚠️  No training data found!")
        print("Please run collect_data.py first to collect hand gesture samples.")
        return
    
    # Load training data
    print("📂 Loading training data...")
    X, y = collector.create_training_dataset()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"\n📊 Data split:")
    print(f"   Training samples: {X_train.shape[0]}")
    print(f"   Testing samples: {X_test.shape[0]}")
    print(f"   Features per sample: {X_train.shape[1]}\n")
    
    # Train model
    print(f"🔧 Training {model_type} model...")
    classifier = GestureClassifier(model_type=model_type)
    classifier.train(X_train, y_train)
    
    # Evaluate on test set
    print(f"\n📈 Model Evaluation:")
    test_accuracy = classifier.model.score(
        classifier.scaler.transform(X_test),
        y_test
    )
    print(f"   Test accuracy: {test_accuracy:.2%}")
    
    # Save model
    model_path = os.path.join(collector.data_dir, f"gesture_model_{model_type}")
    classifier.save_model(model_path)
    
    print(f"\n✓ Model saved successfully!")
    print(f"{'='*60}\n")
    
    return classifier, X_test, y_test

if __name__ == "__main__":
    # Train with Random Forest (good balance)
    classifier, X_test, y_test = train_gesture_model(model_type='random_forest')
    
    # Optional: Train multiple models and compare
    # print("\nTraining SVM...")
    # svm_classifier, _, _ = train_gesture_model(model_type='svm')
    # print("\nTraining Neural Network...")
    # nn_classifier, _, _ = train_gesture_model(model_type='neural_network')
