# hardware/start_button.py

import RPi.GPIO as GPIO
import time

START_PIN = 27  # Change this if need (Physical pin 13)

GPIO.setmode(GPIO.BCM)
GPIO.setup(START_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Active LOW

def wait_for_press():
    print("[START BUTTON] Waiting for start button press...")
    try:
        while GPIO.input(START_PIN) == GPIO.HIGH:
            time.sleep(0.1)
        print("[START BUTTON] Start button pressed! Launching autonomous mode...")
    except KeyboardInterrupt:
        print("[START BUTTON] Interrupted by user.")
        raise

def cleanup():
    GPIO.cleanup(START_PIN)
    print("[START BUTTON] Cleaned up.")
