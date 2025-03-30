# mock/arm.py

import time
from configs.test_scenarios import SCENARIO

print(f"[MAIN] Running SCENARIO: {SCENARIO['name']}")

# Internal state
_arm_down = False

def arm_up():
    global _arm_down
    _arm_down = False
    print("[MOCK ARM] Arm raised.")
    time.sleep(1)

def arm_down():
    global _arm_down
    _arm_down = True
    print("[MOCK ARM] Arm lowered.")
    time.sleep(1)

def stop_arm():
    print("[MOCK ARM] Arm stopped.")

def is_arm_down():
    print(f"[MOCK ARM] is_arm_down() → {_arm_down}")
    return _arm_down
