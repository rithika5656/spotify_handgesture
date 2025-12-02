import cv2
from hand_gesture_model import HandGestureModel

model = HandGestureModel()
x_positions = []

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    lmList = model.get_landmarks(frame)

    if len(lmList) > 0:
        fingers = model.count_fingers(lmList)
        cv2.putText(frame, f"Fingers: {fingers}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        x_positions.append(lmList[0][1])
        if len(x_positions) > 10:
            x_positions.pop(0)

        swipe = model.detect_swipe(x_positions)
        if swipe:
            cv2.putText(frame, swipe, (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3)

    cv2.imshow("Hand Gesture Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
