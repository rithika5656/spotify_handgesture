import cv2
import mediapipe as mp
import math

class HandGestureModel:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils

    def get_landmarks(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        lmList = []

        if results.multi_hand_landmarks:
            handLms = results.multi_hand_landmarks[0]
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

            self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return lmList

    # Count number of fingers open
    def count_fingers(self, lmList):
        if len(lmList) == 0:
            return -1

        fingers = []

        # Thumb
        if lmList[4][1] > lmList[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        tips = [8, 12, 16, 20]
        for tip in tips:
            if lmList[tip][2] < lmList[tip - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers.count(1)

    # Detect swipe
    def detect_swipe(self, x_positions):
        if len(x_positions) < 5:
            return None

        diff = x_positions[-1] - x_positions[0]

        if diff > 50:
            return "SWIPE_RIGHT"
        elif diff < -50:
            return "SWIPE_LEFT"

        return None
