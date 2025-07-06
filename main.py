import cv2
from hand_tracking import detect_hand, draw_landmarks
from mouse_control import move_mouse, click_gesture, drag_gesture, scroll_gesture, double_click_gesture

print("Starting Gesture Control Mouse...")

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("⚠️ Error: Camera not accessible!")
    exit()

# Main loop
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("⚠️ Error: Frame not captured!")
        break

    frame = cv2.flip(frame, 1)
    results = detect_hand(frame)

    if results and results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            try:
                landmarks = hand_landmarks.landmark

                move_mouse(landmarks[8])               # Move using Index Finger
                click_gesture(landmarks)               # Click using Index Finger
                double_click_gesture(landmarks)        # Double Click using Index Finger
                drag_gesture(landmarks)                # Drag using Middle Finger
                scroll_gesture(landmarks)              # Scroll using Thumb

                draw_landmarks(frame, hand_landmarks)
            except Exception as e:
                print(f"❌ Error: {e}")

    cv2.imshow("Gesture Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Camera released. Windows closed.")
