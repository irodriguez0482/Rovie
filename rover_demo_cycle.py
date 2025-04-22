import time
from core import obstacle_avoidance, arm_control_logic
from hardware import gps, motors, force_button, estop, arm
from utils.coordinate_utils import haversine_distance
from utils import map_tracker

def run_demo_mode():
    runTime = 3
    
    motors.init_serial()
    motors.stop_all()
    time.sleep(0.5)
    motors.drive_forward()
    time.sleep(runTime)
    motors.drive_backward()
    time.sleep(runTime)
    motors.turn_left()
    time.sleep(runTime)
    motors.turn_right()
    time.sleep(runTime)
    motors.stop_drive()
    arm.arm_up()
    motors.vibration_on()
    time.sleep(runTime)
    arm.arm_down()
    motors.vibration_off()
    time.sleep(runTime)
    motors.stop_all()
