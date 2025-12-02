"""
TEST MODULE
Test individual components of the gesture control system
"""

import cv2
import numpy as np
from modules.hand_detection import HandDetector
from modules.feature_extraction import FeatureExtractor

def test_camera():
    """Test if camera is working"""
    print("\n" + "="*60)
    print("🎥 Testing Camera...")
    print("="*60)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("✗ Camera not found!")
        return False
    
    print("✓ Camera opened successfully")
    print("Press 'Q' to close the camera test window\n")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("✗ Error reading from camera")
            break
        
        frame_count += 1
        
        # Display info
        cv2.putText(
            frame, f"Camera Test - Frame: {frame_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 255, 0), 2
        )
        cv2.putText(
            frame, "Press Q to quit",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (255, 255, 255), 2
        )
        
        cv2.imshow("Camera Test", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"✓ Camera test completed ({frame_count} frames captured)")
    return True

def test_hand_detection():
    """Test hand detection module"""
    print("\n" + "="*60)
    print("🖐️  Testing Hand Detection (MediaPipe)...")
    print("="*60 + "\n")
    
    try:
        detector = HandDetector()
        print("✓ MediaPipe initialized")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("✗ Camera not available")
            return False
        
        print("Testing hand detection. Position your hand in the camera.")
        print("Press 'Q' to finish test\n")
        
        hand_detected_count = 0
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame_count += 1
            
            frame, landmarks_list = detector.detect_hands(frame)
            
            if len(landmarks_list) > 0:
                hand_detected_count += 1
                cv2.putText(
                    frame, "✓ Hand Detected!",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2
                )
            else:
                cv2.putText(
                    frame, "No hand detected",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2
                )
            
            detection_rate = (hand_detected_count / frame_count * 100) if frame_count > 0 else 0
            cv2.putText(
                frame, f"Detection Rate: {detection_rate:.1f}%",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2
            )
            
            cv2.imshow("Hand Detection Test", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"✓ Hand detection test completed")
        print(f"  - Frames processed: {frame_count}")
        print(f"  - Hands detected: {hand_detected_count}")
        print(f"  - Detection rate: {(hand_detected_count/frame_count*100):.1f}%")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during hand detection test: {e}")
        return False

def test_feature_extraction():
    """Test feature extraction"""
    print("\n" + "="*60)
    print("📊 Testing Feature Extraction...")
    print("="*60 + "\n")
    
    try:
        detector = HandDetector()
        extractor = FeatureExtractor()
        
        print("Testing feature extraction. Show different hand gestures.")
        print("Press 'SPACE' to extract features from detected hand")
        print("Press 'Q' to finish\n")
        
        cap = cv2.VideoCapture(0)
        sample_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame, landmarks_list = detector.detect_hands(frame)
            
            cv2.putText(
                frame, f"Samples extracted: {sample_count}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 255, 0), 2
            )
            cv2.putText(
                frame, "SPACE: Extract | Q: Quit",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2
            )
            
            cv2.imshow("Feature Extraction Test", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' ') and len(landmarks_list) > 0:
                landmarks = landmarks_list[0]
                features = extractor.extract_features(landmarks)
                
                print(f"\n✓ Extracted features (sample {sample_count+1}):")
                print(f"  Feature vector shape: {features.shape}")
                print(f"  Feature values: {features}")
                
                sample_count += 1
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n✓ Feature extraction test completed")
        print(f"  - Samples extracted: {sample_count}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during feature extraction test: {e}")
        return False

def test_all_modules():
    """Run all tests"""
    print("\n\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🧪 GESTURE CONTROL - MODULE TESTING".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    
    tests = [
        ("Camera", test_camera),
        ("Hand Detection", test_hand_detection),
        ("Feature Extraction", test_feature_extraction),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("="*60)
    if all_passed:
        print("\n✓ All tests passed! You're ready to use the system.")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
    print("\n")

if __name__ == "__main__":
    test_all_modules()
