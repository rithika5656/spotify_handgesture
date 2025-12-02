import pyautogui
import time

print("Testing Spotify connection...")
time.sleep(2)

# Focus Spotify window
pyautogui.hotkey('alt', 'tab')  # Switch to Spotify
time.sleep(1)

# Test commands
print("Sending Play/Pause...")
pyautogui.press('space')
time.sleep(2)

print("Sending Next Track...")
pyautogui.hotkey('ctrl', 'right')