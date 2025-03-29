# mock/estop.py

import time
from configs.test_scenarios import SCENARIO

_trigger_time = SCENARIO.get("estop_trigger_time", None)
_start_time = time.time()
_triggered = False

def is_engaged():
    global _triggered
    if _trigger_time is not None:
        now = time.time() - _start_time
        if now >= _trigger_time and not _triggered:
            _triggered = True
            print(f"[MOCK E-STOP] Simulated E-Stop at {now:.1f}s.")
    return _triggered

def cleanup():
    print("[MOCK E-STOP] Cleanup complete.")
