import time
from core import obstacle_avoidance, arm_control_logic
from hardware import gps, motors, force_button, estop
from utils.coordinate_utils import haversine_distance
from utils import map_tracker

def run_demo_mode():
    try:
        motors.init_serial()
        motors.stop_all()
        time.sleep(1)
        motors.drive_forward()
        time.sleep(1)
        motors.drive_backward()
        time.sleep(1)
        motors.turn_left()
        time.sleep(1)
        motors.turn_right()
        time.sleep(1)
        motors.stop_drive()
        arm_control_logic.update_arm_state()
        time.sleep(1)
        arm_control_logic.update_arm_state("reroute")
        time.sleep(1)
        motors.stop_all()

    except KeyboardInterrupt:
        print("[DEMO] Interrupted by user.")
    finally:
        motors.cleanup()
        force_button.cleanup()
        estop.cleanup()
        
try:
    run_demo_mode()
except KeyboardInterrupt:
    print("\n[DEMO] Shutdown via KeyboardInterrupt.")
finally:
    motors.cleanup()