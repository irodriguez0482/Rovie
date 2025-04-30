# core/obstacle_avoidance.py

import time
from hardware import motors, force_button, gps, arm
from utils.logger import log_flagged_gps
from utils.coordinate_utils import haversine_distance
from core import arm_control_logic

# Constants (TODO// move to config/constants.py)
ROVER_LENGTH = 1.0   # in meters
ROVER_WIDTH = 1.0    # in meters
GPS_CHECK_INTERVAL = 0.1  # seconds

# ========== GPS-Based Movement ==========
def move_distance(direction_fn, distance_m):
    """Moves in a direction until the given GPS distance is reached."""
    start = gps.GetCurrentLocation()
    if None in start:
        print("[AVOIDANCE] GPS unavailable. Skipping movement.")
        return

    direction_fn()  # start moving
    while True:
        if force_button.is_pressed():
            print("[AVOIDANCE] Force button triggered during movement! Aborting.")
            motors.stop_drive()
            reroute()  # recursive call to retry
            return

        current = gps.GetCurrentLocation()
        if None in current:
            print("[AVOIDANCE] GPS error, continuing...")
            time.sleep(GPS_CHECK_INTERVAL)
            continue

        traveled = haversine_distance(start, current)
        if traveled >= distance_m:
            break

        time.sleep(GPS_CHECK_INTERVAL)

    motors.stop_drive()

# ========== Safe Turns ==========
def turn_left_90():
    _safe_turn(motors.turn_left, duration=1.0)

def turn_right_90():
    _safe_turn(motors.turn_right, duration=1.0)

def _safe_turn(turn_fn, duration=1.0):
    turn_fn()
    elapsed = 0
    step = 0.1
    while elapsed < duration:
        if force_button.is_pressed():
            print("[AVOIDANCE] Force button during turn! Aborting.")
            motors.stop_drive()
            reroute()
            return
        time.sleep(step)
        elapsed += step
    motors.stop_drive()

# ========== Reroute Logic ==========
def reroute(retry_depth=0, max_retries=3):
    print(f"[AVOIDANCE] Obstacle detected. Starting reroute sequence (attempt {retry_depth + 1})")

    # Step 1: Log the current GPS location
    lat, lon = gps.GetCurrentLocation()
    if lat and lon:
        log_flagged_gps(lat, lon, note=f"Obstacle encounter (attempt {retry_depth + 1})")

    # Step 2: Stop movement and vibration
    motors.stop_drive()
    motors.vibration_off()

    # Step 3: Raise the arm
    arm.arm_up()
    time.sleep(1)
    print("[AVOIDANCE] Arm raised.")

    arm_control_logic.update_arm_state("reroute")

    # Step 4: Back up one rover length
    move_distance(motors.drive_backward, ROVER_LENGTH)

    # Step 5: Turn 90° left
    turn_left_90()

    # Step 6: Move sideways (1 rover width)
    move_distance(motors.drive_forward, ROVER_WIDTH)

    # Step 7: Turn 90° right
    turn_right_90()

    # Step 8: Move forward (2 rover lengths)
    move_distance(motors.drive_forward, ROVER_LENGTH * 2)

    # Step 9: Rejoin path - turn right
    turn_right_90()

    # Step 10: Move forward (1 rover width)
    move_distance(motors.drive_forward, ROVER_WIDTH)

    # Step 11: Turn left to face original path
    turn_left_90()

    # Step 12: Lower arm and enable vibration if ready
    arm.arm_down()
    if arm.is_arm_down():
        motors.vibration_on()
        arm_control_logic.update_arm_state("clearing")
    else:
        print("[AVOIDANCE] Arm not fully down — skipping vibration.")

    # Step 13: Probe forward slightly
    move_distance(motors.drive_forward, ROVER_LENGTH / 2)

    # Step 14: Check if still blocked
    if force_button.is_pressed():
        print("[AVOIDANCE] Still blocked after reroute.")
        if retry_depth < max_retries:
            reroute(retry_depth=retry_depth + 1)
        else:
            print("[AVOIDANCE] Max retries reached. Logging as impassable.")
            lat, lon = gps.GetCurrentLocation()
            if lat and lon:
                log_flagged_gps(lat, lon, note="Impassable obstacle (max retries reached)")
            motors.stop_all()
    else:
        print("[AVOIDANCE] Obstacle avoided. Rejoined original path.")
