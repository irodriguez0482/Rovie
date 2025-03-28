import serial
import time
import RPi.GPIO as GPIO

#6 bit command: 0-0-0-0-0-0
# bit 1: enable drive motors
#       0 - off
#       1 - on
# bit 2&3: drive direction
#       00 - forward
#       01 - backward
#       10 - left
#       11 - right
# bit 4: enable plow motor
#       0 - off
#       1 - on
# bit 5: plow direction
#       0 - up
#       1 - down
#bit 6: enable viration
#       0 - off
#       1 - on

STOP = 000000

direction = {
    "FORWARD": "100000",
    "BACKWARD": "101000",
    "STOP": "000000"
}

turnDirection = {
    "LEFT": "110000",
    "RIGHT": "111000",
    "STOP": "000000"
}

arm = {
    "UP": "000100",
    "DOWN": "000110",
    "STOP": "000000"
}

vibration = {
    "ON": "000001",
    "OFF": "000000"
}

def send_command(ser, command):
    """Send a command to the Arduino."""
    print(f"\n[DEBUG] Sending command: {command}")
    ser.write((command + "\n").encode())  # Send the command with newline
    time.sleep(0.1)  # Give Arduino time to process

def receive_from_arduino(ser):
    """Continuously read responses from the Arduino."""
    while ser.in_waiting == 0:
        print("[DEBUG] Waiting for Arduino")
        time.sleep(0.1)
    while ser.in_waiting > 0:
        response = ser.readline().decode(errors='replace').strip()
        print(f"[Arduino] {response}")    
