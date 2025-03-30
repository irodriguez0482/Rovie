# hardware/force_button.py

import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17  # BCM numbering (physical pin 11)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def is_pressed():
    """Returns True if the force button is currently pressed."""
    return GPIO.input(BUTTON_PIN) == GPIO.LOW

def cleanup():
    """Call this at program shutdown to clean up GPIO."""
    GPIO.cleanup()
