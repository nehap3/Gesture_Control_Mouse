import pyautogui
import math
import time

screen_width, screen_height = pyautogui.size()
prev_x, prev_y = None, None
last_click_time = 0
dragging = False
deadzone = 5  # Threshold for smoother movement

# Function to move the mouse based on index finger position
def move_mouse(index_finger_tip):
    global prev_x, prev_y
    screen_x = int(index_finger_tip.x * screen_width)
    screen_y = int(index_finger_tip.y * screen_height)

    if prev_x is None or prev_y is None:
        prev_x, prev_y = screen_x, screen_y

    # Smoother movement based on deadzone threshold
    if abs(screen_x - prev_x) > deadzone or abs(screen_y - prev_y) > deadzone:
        smooth_x = prev_x + (screen_x - prev_x) * 0.2
        smooth_y = prev_y + (screen_y - prev_y) * 0.2
        pyautogui.moveTo(int(smooth_x), int(smooth_y), duration=0.03)
        prev_x, prev_y = smooth_x, smooth_y

# Function to detect click gesture (index finger up while others are down)
def click_gesture(landmarks):
    global last_click_time
    fingers_up = is_finger_up(landmarks, 8) and not any([
        is_finger_up(landmarks, 12),
        is_finger_up(landmarks, 16),
        is_finger_up(landmarks, 20)
    ])
    if fingers_up:
        current_time = time.time()
        if current_time - last_click_time > 1:
            pyautogui.click()
            last_click_time = current_time
            print("Click!")

# Function to detect double-click gesture
def double_click_gesture(landmarks):
    global last_click_time
    current_time = time.time()
    if is_finger_up(landmarks, 8) and not any([
        is_finger_up(landmarks, 12),
        is_finger_up(landmarks, 16),
        is_finger_up(landmarks, 20)
    ]):
        if current_time - last_click_time < 0.3:
            pyautogui.doubleClick()
            print("Double Click!")
        last_click_time = current_time

# Function to handle drag gesture (middle finger up)
def drag_gesture(landmarks):
    global dragging
    ring_tip = landmarks[16]
    screen_x = int(ring_tip.x * screen_width)
    screen_y = int(ring_tip.y * screen_height)

    if is_finger_up(landmarks, 16):
        if not dragging:
            pyautogui.mouseDown(x=screen_x, y=screen_y)
            dragging = True
            print("Drag Start")
        else:
            pyautogui.moveTo(screen_x, screen_y, duration=0.01)
    else:
        if dragging:
            pyautogui.mouseUp()
            dragging = False
            print("Drag End")

# Scroll Gesture using thumb and index finger
scroll_threshold = 0.05

def scroll_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    y_diff = thumb_tip.y - index_tip.y

    print(f"Thumb Y: {thumb_tip.y}, Index Y: {index_tip.y}, Y Diff: {y_diff}")

    if abs(y_diff) > scroll_threshold:
        if y_diff > 0:
            pyautogui.scroll(-50)
            print("Scrolling Down...")
        elif y_diff < 0:
            pyautogui.scroll(50)
            print("Scrolling Up...")

# Helper function to check if a finger is up
def is_finger_up(landmarks, tip_id):
    return landmarks[tip_id].y < landmarks[tip_id - 2].y
