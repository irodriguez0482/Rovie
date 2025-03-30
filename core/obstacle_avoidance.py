# core/obstacle_avoidance.py

import time
from hardware import motors, force_button, gps, arm
from utils.logger import log_flagged_gps
from utils.coordinate_utils import haversine_distance
from core import arm_control_logic

# Constants (can be moved to config/constants.py)
ROVER_LENGTH = 1.0   # in meters
ROVER_WIDTH = 1.0    # in meters
TIME_PER_METER = 1.5  # seconds per meter of travel (adjust experimentally)

def drive_forward_distance(meters):
    motors.drive_forward()
    time.sleep(meters * TIME_PER_METER)
    motors.stop_drive()

def drive_backward_distance(meters):
    motors.drive_backward()
    time.sleep(meters * TIME_PER_METER)
    motors.stop_drive()

def turn_left_90():
    motors.turn_left()
    time.sleep(1)  # Adjust this based on how long it takes to rotate 90°
    motors.stop_drive()

def turn_right_90():
    motors.turn_right()
    time.sleep(1)
    motors.stop_drive()

def reroute(retry_depth=0, max_retries=3):
    print(f"[AVOIDANCE] Obstacle detected. Starting reroute sequence (attempt {retry_depth + 1})")

    # Step 1: Log the current GPS location
    lat, lon = gps.GetCurrentLocation()
    if lat and lon:
        log_flagged_gps(lat, lon, note=f"Obstacle encounter (attempt {retry_depth + 1})")

    # Step 2: Stop movement and vibration
    motors.stop_drive()
    motors.vibration_off()

    # Step 3: Raise the arm first
    arm.arm_up()
    time.sleep(1)
    print("[AVOIDANCE] Arm raised.")

    # Early in reroute:
    arm_control_logic.update_arm_state("reroute")

    # Step 4: Back up one rover length
    drive_backward_distance(ROVER_LENGTH)

    # Step 5: Turn 90° left
    turn_left_90()

    # Step 6: Move sideways (1 rover width)
    drive_forward_distance(ROVER_WIDTH)

    # Step 7: Turn 90° right
    turn_right_90()

    # Step 8: Move forward (2 rover lengths)
    drive_forward_distance(ROVER_LENGTH * 2)

    # Step 9: Rejoin path - turn right
    turn_right_90()

    # Step 10: Move forward (1 rover width)
    drive_forward_distance(ROVER_WIDTH)

    # Step 11: Turn left to face original path
    turn_left_90()

    # Step 12: Attempt to lower the arm
    arm.arm_down()
    if arm.is_arm_down():
        motors.vibration_on()
        # After turning and getting into position:
        arm_control_logic.update_arm_state("clearing")
    else:
        print("Arm not fully down — skipping vibration.")

    # Step 13: Probe forward slightly to rejoin path
    drive_forward_distance(ROVER_LENGTH / 2)

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
