import pyautogui
import time

print("🎵 Testing Spotify Connection...")
print("Make sure Spotify is OPEN and PLAYING music!")
print("Testing in 3 seconds...")
time.sleep(3)

print("🔄 Switching to Spotify window...")
pyautogui.hotkey('alt', 'tab')  # Switch to Spotify
time.sleep(2)

print("⏯️ Sending Play/Pause command...")
pyautogui.press('space')
time.sleep(2)

print("⏭️ Sending Next Track command...")
pyautogui.hotkey('ctrl', 'right')
time.sleep(2)

print("⏮️ Sending Previous Track command...")
pyautogui.hotkey('ctrl', 'left')

print("✅ Test complete! Did Spotify respond?")