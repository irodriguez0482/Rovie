import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17  # BCM numbering (physical pin 11) connect other end to GND

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #No resistor

pressed = False

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            if not pressed:
                print("Button pressed")
                pressed = True
        else:
            if pressed:
                print("Button released")
                pressed = False

        time.sleep(0.05)  # debounce + responsiveness

except KeyboardInterrupt:
    print("Stopped by User")

finally:
    GPIO.cleanup()

