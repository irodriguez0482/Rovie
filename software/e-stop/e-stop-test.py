import RPi.GPIO as GPIO
import time

# Define GPIO pin
ESTOP_PIN = 18  # GPIO18 (Physical Pin 12)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # If using NC

def check_estop():
    try:
        while True:
            if GPIO.input(ESTOP_PIN) == GPIO.HIGH:
                print("E-Stop RELEASED (Running)")
            else:
                print("E-Stop PRESSED (STOP!)")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nExiting...")
        GPIO.cleanup()

# Run the test
check_estop()