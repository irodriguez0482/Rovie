# core/autonomous.py

import time
from core import obstacle_avoidance, arm_control_logic
from hardware import gps, motors, force_button, estop
from utils.coordinate_utils import haversine_distance

def clear_line(line_length_m=3.0):
    """Drives forward until the rover travels the given distance or hits an obstacle or E-Stop."""
    print(f"[AUTONOMOUS] Starting new line: target = {line_length_m} meters")

    start_coords = gps.GetCurrentLocation()
    if None in start_coords:
        print("[ERROR] GPS fix failed. Cannot start line.")
        return

    arm_control_logic.update_arm_state("clearing")
    motors.drive_forward()

    while True:
        if estop.is_engaged():
            print("[AUTONOMOUS] E-Stop triggered! Stopping all motion.")
            motors.stop_all()
            return

        if force_button.is_pressed():
            print("[AUTONOMOUS] Obstacle detected! Initiating reroute.")
            motors.stop_drive()
            obstacle_avoidance.reroute()
            motors.drive_forward()  # Resume forward movement

        current_coords = gps.GetCurrentLocation()
        if None in current_coords:
            print("[WARNING] GPS signal lost, retrying...")
            time.sleep(0.2)
            continue

        distance = haversine_distance(start_coords, current_coords)
        print(f"[AUTONOMOUS] Distance traveled: {distance:.2f}m")

        if distance >= line_length_m:
            print("[AUTONOMOUS] Target reached. Stopping.")
            break

        time.sleep(0.2)

    motors.stop_all()
    time.sleep(1)

def run_autonomous_mode():
    try:
        motors.init_serial()
        print("[AUTONOMOUS] Beginning 3x3 grid clearing...")

        for i in range(6):
            clear_line(line_length_m=3.0)
            # Add turning logic here later

        print("[AUTONOMOUS] Grid complete.")

    except KeyboardInterrupt:
        print("[AUTONOMOUS] Interrupted by user.")
    finally:
        motors.cleanup()
        force_button.cleanup()
        estop.cleanup()
