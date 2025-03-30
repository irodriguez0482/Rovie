# mock/start_button.py

import time

def wait_for_press():
    print("[MOCK START BUTTON] Simulating wait for start button press...")
    time.sleep(1.5)  # Simulate someone pressing the button after a second
    print("[MOCK START BUTTON] Simulated start button press!")

def cleanup():
    print("[MOCK START BUTTON] Cleanup complete.")
