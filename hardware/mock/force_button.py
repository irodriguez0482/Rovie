# mock/force_button.py

import time
from configs.test_scenarios import SCENARIO

print(f"[MAIN] Running SCENARIO: {SCENARIO['name']}")

_press_times = SCENARIO.get("force_button_press_times", [])
_start_time = time.time()
_triggered_times = set()

def is_pressed():
    """Returns True if it's time to simulate a force button press."""
    global _triggered_times
    now = time.time() - _start_time
    for t in _press_times:
        if t <= now < t + 0.5 and t not in _triggered_times:
            print(f"[MOCK BUTTON] Simulated force button press at {now:.1f}s.")
            _triggered_times.add(t)
            return True
    return False

def cleanup():
    print("[MOCK BUTTON] Cleaned up.")
