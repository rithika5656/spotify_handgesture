import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

# Helper: distance between two landmarks
def dist(a, b):
    return np.linalg.norm(np.array([a.x, a.y]) - np.array([b.x, b.y]))

# Gesture logic
def detect_gesture(landmarks):
    thumb = landmarks[4]
    index = landmarks[8]
    middle = landmarks[12]
    ring = landmarks[16]
    pinky = landmarks[20]

    wrist = landmarks[0]

    # Pinch (Index + Thumb close)
    if dist(thumb, index) < 0.05:
        return "PINCH"

    # Fist (all fingers close)
    if (dist(index, wrist) < 0.12 and 
        dist(middle, wrist) < 0.12 and
        dist(ring, wrist) < 0.12 and
        dist(pinky, wrist) < 0.12):
        return "FIST"

    # Palm open (all fingers far)
    if (dist(index, wrist) > 0.18 and
        dist(middle, wrist) > 0.18 and
        dist(ring, wrist) > 0.18 and
        dist(pinky, wrist) > 0.18):
        return "PALM"

    return None

# Action mapping
def perform_action(gesture):
    if gesture == "PALM":
        pyautogui.press("playpause")
        print("▶️ Play / Pause")

    elif gesture == "PINCH":
        pyautogui.press("volumedown")
        print("🔉 Volume Down")

    elif gesture == "FIST":
        pyautogui.press("volumeup")
        print("🔊 Volume Up")

# Real-time CV pipeline
cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    last_action_time = time.time()

    while True:
        success, frame = cap.read()
        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for lm in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)

                gesture = detect_gesture(lm.landmark)

                # Prevent multiple triggers
                if gesture and time.time() - last_action_time > 1:
                    perform_action(gesture)
                    last_action_time = time.time()

        cv2.imshow("Spotify Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
