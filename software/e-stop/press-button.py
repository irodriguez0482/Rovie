import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17  # Replace with actual GPIO pin number

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pressed = False

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            if not pressed:
                print("Button pressed")
                pressed = True
            print("Button is still pressed")
            time.sleep(1)
        else:
            if pressed:
                print("Button was released")
                pressed = False
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopped by User")

finally:
    GPIO.cleanup()
