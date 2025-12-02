import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

def get_fingers_status(hand):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    # thumb - compare x to IP (works for mirrored webcam)
    fingers.append(1 if hand.landmark[tips[0]].x < hand.landmark[tips[0]-1].x else 0)
    # other fingers - tip.y < pip.y
    for tip in tips[1:]:
        fingers.append(1 if hand.landmark[tip].y < hand.landmark[tip-2].y else 0)
    return fingers  # [thumb,index,middle,ring,pinky]

def detect_thumb_special(hand, fingers):
    thumb_tip = hand.landmark[4].y
    thumb_ip = hand.landmark[3].y
    wrist = hand.landmark[0].y
    # Only consider thumb UP/DOWN when other fingers folded
    if thumb_tip < wrist and thumb_ip < wrist and fingers[1:] == [0,0,0,0]:
        return "THUMBS_UP"
    if thumb_tip > wrist and thumb_ip > wrist and fingers[1:] == [0,0,0,0]:
        return "THUMBS_DOWN"
    return None

def map_gesture(f, thumb_special):
    # Thumb special first (strict)
    if thumb_special:
        return thumb_special
    # POINT: index up only AND thumb folded (avoid thumb interference)
    if f[0] == 0 and f[1] == 1 and f[2] == 0 and f[3] == 0 and f[4] == 0:
        return "POINT"
    # V_SIGN: thumb folded AND index+middle up
    if f[0] == 0 and f[1] == 1 and f[2] == 1 and f[3] == 0 and f[4] == 0:
        return "V_SIGN"
    # FIST / PALM
    if f[1:] == [0,0,0,0]:
        return "FIST"
    if f[1:] == [1,1,1,1]:
        return "PALM"
    return "UNKNOWN"

def perform_action(gesture):
    print("ACTION TRIGGERED ->", gesture)

    if gesture == "PALM":
        pyautogui.press("volumeup")

    elif gesture == "FIST":
        pyautogui.press("volumedown")

    elif gesture == "POINT":
        pyautogui.hotkey("ctrl", "right")   

    elif gesture == "V_SIGN":
        pyautogui.hotkey("ctrl", "left")    

    elif gesture == "THUMBS_UP":
        pyautogui.press("playpause")

    elif gesture == "THUMBS_DOWN":
        pyautogui.press("playpause")

def draw_status(frame, f, gesture):
    h, w, _ = frame.shape
    # fingers text
    cv2.putText(frame, f"Fingers: {f}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,0), 2)
    cv2.putText(frame, f"Gesture: {gesture}", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
    # small circles for index,middle,thumb
    color_on = (0,255,0); color_off = (0,0,255)
    # thumb
    cv2.circle(frame, (60,90), 10, color_on if f[0] else color_off, -1)
    cv2.putText(frame, "Thumb", (75,95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),1)
    # index
    cv2.circle(frame, (60,130), 10, color_on if f[1] else color_off, -1)
    cv2.putText(frame, "Index", (75,135), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),1)
    # middle
    cv2.circle(frame, (60,170), 10, color_on if f[2] else color_off, -1)
    cv2.putText(frame, "Middle", (75,175), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),1)

def main():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6)
    cooldown = 0.6
    last_action = 0.0
    print("DEBUG MODE: prints fingers & mapped gesture each frame.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame,1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)
        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                f = get_fingers_status(hand_landmarks)
                thumb_special = detect_thumb_special(hand_landmarks, f)
                gesture = map_gesture(f, thumb_special)
                # debug prints
                print("Fingers:", f, "| ThumbSpecial:", thumb_special, "| Mapped:", gesture)
                # action with cooldown (continuous)
                if gesture != "UNKNOWN" and time.time() - last_action > cooldown:
                    perform_action(gesture)
                    last_action = time.time()
                draw_status(frame, f, gesture)
        cv2.imshow("DEBUG - Spotify Gesture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
