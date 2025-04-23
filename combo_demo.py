import time
import keyboard  # pip install keyboard

#including keyboard
import RPi.GPIO as GPIO
demo_button=7 #physical pin 26

from core import obstacle_avoidance, arm_control_logic
from hardware import gps, motors, force_button, estop, arm
from utils.coordinate_utils import haversine_distance
from utils import map_tracker
from rover_demo_cycle import run_demo_mode

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(demo_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def is_Pressed():
    """Returns True if the demo button is currently pressed."""
    return GPIO.input(demo_button) == GPIO.LOW

def cleanUp():
    """Call this at program shutdown to clean up GPIO."""
    GPIO.cleanup()
    
def print_controls():
    print("\n[DEMO] Press a key to activate a function. Press 'q' to quit.\n")
    print("""
    Controls:
    w - Drive Forward
    s - Drive Backward
    a - Turn Left
    d - Turn Right
    x - Stop All
    u - Arm Up
    j - Arm Down
    v - Vibration On
    b - Vibration Off
    q - Quit
    """)

def run_keyboard_Demo():
    print_controls()

    motors.init_serial()
    motors.stop_all()

    try:
        while True:
            if keyboard.is_pressed('w'):
                print(chr(27) + "[2J")
                print("[DEMO] Driving forward")
                motors.drive_forward()
                time.sleep(0.5)
                print_controls()

            elif keyboard.is_pressed('s'):
                print(chr(27) + "[2J")
                print("[DEMO] Driving backward")
                motors.drive_backward()
                time.sleep(0.5)
                print_controls()

            elif keyboard.is_pressed('a'):
                print(chr(27) + "[2J")
                print("[DEMO] Turning left")
                motors.turn_left()
                time.sleep(0.5)
                print_controls()

            elif keyboard.is_pressed('d'):
                print(chr(27) + "[2J")
                print("[DEMO] Turning right")
                motors.turn_right()
                time.sleep(0.5)
                print_controls()

            elif keyboard.is_pressed('x'):
                print(chr(27) + "[2J")
                print("[DEMO] Stopping all motors")
                motors.stop_all()
                time.sleep(0.5)
                print_controls()

            elif keyboard.is_pressed('u'):
                print(chr(27) + "[2J")
                print("[DEMO] Arm Up")
                arm.arm_up()
                time.sleep(0.5)
                print_controls()

            elif keyboard.is_pressed('j'):
                print(chr(27) + "[2J")
                print("[DEMO] Arm Down")
                arm.arm_down()
                time.sleep(0.5)
                print_controls()

            elif keyboard.is_pressed('v'):
                print("[DEMO] Vibration ON (1s pulse)")
                motors.vibration_on()
                time.sleep(1)
                motors.vibration_off()
                print("[DEMO] Vibration OFF (auto)")
                time.sleep(0.5)  # To avoid accidental re-trigger

            elif keyboard.is_pressed('q'):
                print(chr(27) + "[2J")
                print("[DEMO] Quitting demo mode.")
                break
            elif is_Pressed():
                print(chr(27) + "[2J")
                print("Rover Demo Started!")
                run_demo_mode()
                time.sleep(0.5)
                print_controls()
                time.sleep(0.1)  # Prevent CPU overuse

            if hasattr(motors, "ser"):
                if motors.ser.in_waiting > 0:
                    response = motors.ser.readline().decode(errors="replace").strip()
                    print(f"[Arduino] {response}")

    except KeyboardInterrupt:
        print("[DEMO] Interrupted by user.")
    finally:
        motors.cleanup()
        force_button.cleanup()
        estop.cleanup()
        cleanUp()

# Run the keyboard demo
if __name__ == "__main__":
    run_keyboard_Demo()
