# hardware/arm.py

import time
from hardware import motors

# Time in seconds to allow arm to reach full up/down
DEFAULT_ARM_MOVEMENT_TIME = 1.0  # Adjust as needed

def arm_up():
    """Raises the arm using motor control."""
    motors.arm_up()
    time.sleep(DEFAULT_ARM_MOVEMENT_TIME)
    stop_arm()
    print("[ARM] Raised.")

def arm_down():
    """Lowers the arm using motor control."""
    motors.arm_down()
    time.sleep(DEFAULT_ARM_MOVEMENT_TIME)
    stop_arm()
    print("[ARM] Lowered.")

def stop_arm():
    """Stops the arm movement."""
    motors.stop_arm()

def is_arm_down():
    """
    Placeholder for future arm position sensor.

    Returns True if the arm is fully lowered.
    Replace this logic with real sensor input once integrated.
    """
    # TODO: Replace this with real sensor reading from Arduino or GPIO
    return True
