# mock/gps.py

from configs.test_scenarios import SCENARIO
import time

# Initial GPS location
_current_lat = 28.602000
_current_lon = -81.198000

# Simulated distance step
GPS_STEP_METERS = 0.5
LAT_STEP = 0.0000089 * GPS_STEP_METERS

# Scenario-driven signal loss
_fail_times = SCENARIO.get("gps_fail_times", [])
_start_time = time.time()

def GetCurrentLocation():
    """Simulates GPS data, returns (None, None) if GPS fails at a given time."""
    global _current_lat

    now = time.time() - _start_time
    for t in _fail_times:
        if t <= now < t + 1:
            print(f"[MOCK GPS] Signal lost at {now:.1f}s!")
            return (None, None)

    _current_lat += LAT_STEP
    return (_current_lat, _current_lon)
