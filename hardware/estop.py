# hardware/estop.py

import RPi.GPIO as GPIO

ESTOP_PIN = 18  # BCM pin (adjust to your setup)

GPIO.setmode(GPIO.BCM)
GPIO.setup(ESTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def is_engaged():
    """Returns True if E-Stop button is currently pressed."""
    return GPIO.input(ESTOP_PIN) == GPIO.LOW

def cleanup():
    GPIO.cleanup()
