import serial
import time
import RPi.GPIO as GPIO

# Serial Communication Settings
SERIAL_PORT = "/dev/ttyACM2"  # Update if necessary (e.g., "COM3" for Windows)
BAUD_RATE = 9600
COMMAND_RUNNING = "110000"  # Command when running
COMMAND_ESTOP = "000000"  # Command when E-Stop is pressed

# E-Stop GPIO Configuration
ESTOP_PIN = 18  # GPIO18 (Physical Pin 12)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Internal pull-up

def send_command(ser, command):
    """Send a command to the Arduino."""
    print(f"\n[DEBUG] Sending command: {command}")
    ser.write((command + "\n").encode())  # Send the command with newline
    time.sleep(0.1)  # Give Arduino time to process

def receive_from_arduino(ser):
    """Continuously read responses from the Arduino."""
    while ser.in_waiting > 0:
        response = ser.readline().decode(errors='replace').strip()
        print(f"[Arduino] {response}")

def main():
    """Continuously send commands while checking E-Stop status."""
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            while True:
                # Always read any incoming messages from Arduino
                receive_from_arduino(ser)

                if GPIO.input(ESTOP_PIN) == GPIO.LOW:
                    print("E-Stop PRESSED! Sending STOP command!")
                    send_command(ser, COMMAND_ESTOP)  # Send STOP command
                    while GPIO.input(ESTOP_PIN) == GPIO.LOW:
                        receive_from_arduino(ser)  # Keep receiving messages while stopped
                        time.sleep(0.5)  # Poll every 0.5 seconds

                    print("E-Stop RELEASED. Resuming operation...")

                # Send normal command when E-Stop is NOT pressed
                send_command(ser, COMMAND_RUNNING)
                receive_from_arduino(ser)  # Read Arduino responses
                time.sleep(5)  # Wait 5 seconds before sending the next command

    except serial.SerialException as e:
        print("[ERROR] Serial communication issue:", e)
    except KeyboardInterrupt:
        print("\n[INFO] Exiting... Cleaning up GPIO.")
        GPIO.cleanup()

if __name__ == "__main__":
    print("[INFO] Starting communication with Arduino...")
    main()