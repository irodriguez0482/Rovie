# core/autonomous.py

import time
from core import obstacle_avoidance, arm_control_logic
from hardware import gps, motors, force_button, estop, arm
from utils.coordinate_utils import haversine_distance
from utils import map_tracker

def clear_line(line_length_m=3.0) -> bool:
    print(f"[AUTONOMOUS] Starting new line: target = {line_length_m} meters")

    # start_coords = gps.GetCurrentLocation()
    # if None in start_coords:
    #     print("[ERROR] GPS fix failed. Cannot start line.")
    #     return False

    obstacle_encountered = False

    arm_control_logic.update_arm_state("clearing")
    motors.stop_all()
    motors.drive_forward()
    arm.arm_up()
    motors.vibration_on()

    while True:
        if estop.is_engaged():
            print("[AUTONOMOUS] E-Stop triggered! Stopping all motion.")
            motors.stop_all()
            return False

        if force_button.is_pressed():
            print("[AUTONOMOUS] Obstacle detected! Initiating reroute.")
            motors.stop_drive()
            obstacle_avoidance.reroute()
            motors.drive_forward()
            obstacle_encountered = True

        # current_coords = gps.GetCurrentLocation()
        # if None in current_coords:
        #     print("[WARNING] GPS signal lost, retrying...")
        #     time.sleep(0.2)
        #     continue

        # distance = haversine_distance(start_coords, current_coords)
        # print(f"[AUTONOMOUS] Distance traveled: {distance:.2f}m")

        # if distance >= line_length_m:
        #     print("[AUTONOMOUS] Target reached. Stopping.")
        #     break

        time.sleep(0.2)

    motors.stop_all()
    time.sleep(1)

    return not obstacle_encountered  # True if line was clear, False if reroute happened

def run_autonomous_mode():
    try:
        motors.init_serial()
        print("[AUTONOMOUS] Beginning 3x3 grid clearing...")

        for i in range(6):
            success = clear_line(line_length_m=3.0)

            # Update map
            row = i
            col = 0
            status = map_tracker.CLEAR if success else map_tracker.OBSTACLE
            map_tracker.mark_cell(row, col, status)

            # TODO: add turning logic later here

        print("[AUTONOMOUS] Grid complete.")
        map_tracker.print_map()
        map_tracker.save_map_to_csv()

    except KeyboardInterrupt:
        print("[AUTONOMOUS] Interrupted by user.")
    finally:
        motors.cleanup()
        force_button.cleanup()
        estop.cleanup()
