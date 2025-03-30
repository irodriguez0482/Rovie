# core/autonomous.py

import time
from core import obstacle_avoidance, arm_control_logic
from hardware import gps, motors, force_button, estop
from utils.coordinate_utils import haversine_distance
from utils import map_tracker

def clear_line(line_length_m=3.0) -> bool:
    ...
    obstacle_encountered = False
    ...
    if force_button.is_pressed():
        print("[AUTONOMOUS] Obstacle detected! Initiating reroute.")
        motors.stop_drive()
        obstacle_avoidance.reroute()
        motors.drive_forward()
        obstacle_encountered = True
    ...
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
            row = i  # You could change this if you want column-based motion later
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
