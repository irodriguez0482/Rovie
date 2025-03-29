# tests/test_force_button.py

import time
from hardware import force_button

print("Testing force button (press and release)...")
print("Press Ctrl+C to stop.\n")

try:
    last_state = False
    while True:
        current = force_button.is_pressed()
        if current != last_state:
            if current:
                print("[BUTTON] Pressed")
            else:
                print("[BUTTON] Released")
            last_state = current

        time.sleep(0.05)  # debounce + responsiveness

except KeyboardInterrupt:
    print("\n[TEST] Force button test stopped by user.")

finally:
    force_button.cleanup()
