import time
import keyboard  # pip install keyboard
from core import obstacle_avoidance, arm_control_logic
from hardware import gps, motors, force_button, estop, arm
from utils.coordinate_utils import haversine_distance
from utils import map_tracker

def run_keyboard_demo():
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

    motors.init_serial()
    motors.stop_all()



    try:
        while True:
            if keyboard.is_pressed('w'):
                print("[DEMO] Driving forward")
                motors.drive_forward()
                time.sleep(0.5)

            elif keyboard.is_pressed('s'):
                print("[DEMO] Driving backward")
                motors.drive_backward()
                time.sleep(0.5)

            elif keyboard.is_pressed('a'):
                print("[DEMO] Turning left")
                motors.turn_left()
                time.sleep(0.5)

            elif keyboard.is_pressed('d'):
                print("[DEMO] Turning right")
                motors.turn_right()
                time.sleep(0.5)

            elif keyboard.is_pressed('x'):
                print("[DEMO] Stopping all motors")
                motors.stop_all()
                time.sleep(0.5)

            elif keyboard.is_pressed('u'):
                print("[DEMO] Arm Up")
                arm.arm_up()
                time.sleep(0.5)

            elif keyboard.is_pressed('j'):
                print("[DEMO] Arm Down")
                arm.arm_down()
                time.sleep(0.5)

            elif keyboard.is_pressed('v'):
                print("[DEMO] Vibration ON (1s pulse)")
                motors.vibration_on()
                time.sleep(1)
                motors.vibration_off()
                print("[DEMO] Vibration OFF (auto)")
                time.sleep(0.5)  # To avoid accidental re-trigger

            elif keyboard.is_pressed('q'):
                print("[DEMO] Quitting demo mode.")
                break

            if hasattr(motors, "ser"):
                if motors.ser.in_waiting > 0:
                    response = motors.ser.readline().decode(errors="replace").strip()
                    print(f"[Arduino] {response}")

            time.sleep(0.1)  # Prevent CPU overuse

    except KeyboardInterrupt:
        print("[DEMO] Interrupted by user.")
    finally:
        motors.cleanup()
        force_button.cleanup()
        estop.cleanup()

# Run the keyboard demo
if __name__ == "__main__":
    run_keyboard_demo()
