# hardware/motors.py

import serial
import time

# ========== CONFIG ==========
SERIAL_PORT = "/dev/ttyACM0"  # Update if needed
BAUD_RATE = 9600

ser = None  # Serial connection object

# ========== COMMAND STATE ==========
command_bits = {
    "motor_enable": 0,
    "drive_dir": "00",    # 00 = forward, 01 = back, 10 = left, 11 = right
    "plow_enable": 0,
    "plow_dir": 0,         # 0 = up, 1 = down
    "vibration": 0
}

# ========== SERIAL INIT ==========
def init_serial():
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        print("[MOTORS] Serial initialized.")
    except serial.SerialException as e:
        print("[ERROR] Could not open serial port:", e)
        if 'log_error' in globals():
            log_error(f"Serial error: {e}")

def cleanup():
    if ser:
        ser.close()
    print("[MOTORS] Serial connection closed.")

# ========== COMMAND BUILDER ==========
def build_command():
    bits = (
        str(command_bits["motor_enable"]) +
        command_bits["drive_dir"] +
        str(command_bits["plow_enable"]) +
        str(command_bits["plow_dir"]) +
        str(command_bits["vibration"])
    )
    return bits

def send_current_command():
    command = build_command()
    _send_to_arduino(command)

def _send_to_arduino(cmd):
    if ser:
        print(f"[MOTORS] Sending command: {cmd}")
        ser.write((cmd + "\n").encode())
        time.sleep(0.1)
        while ser.in_waiting > 0:
            response = ser.readline().decode(errors="replace").strip()
            print(f"[Arduino] {response}")

# ========== HIGH-LEVEL MOVEMENT ==========

# Drive
def drive_forward():
    command_bits["motor_enable"] = 1
    command_bits["drive_dir"] = "00"
    send_current_command()

def drive_backward():
    command_bits["motor_enable"] = 1
    command_bits["drive_dir"] = "01"
    send_current_command()

def turn_left():
    command_bits["motor_enable"] = 1
    command_bits["drive_dir"] = "10"
    send_current_command()

def turn_right():
    command_bits["motor_enable"] = 1
    command_bits["drive_dir"] = "11"
    send_current_command()

def stop_drive():
    command_bits["motor_enable"] = 0
    command_bits["drive_dir"] = "00"
    send_current_command()
    
# Arm
def arm_up():
    command_bits["plow_enable"] = 1
    command_bits["plow_dir"] = 1
    send_current_command()
    
def arm_up():
    command_bits["plow_enable"] = 1
    command_bits["plow_dir"] = 0
    send_current_command()

# Vibration
def vibration_on():
    command_bits["vibration"] = 1
    send_current_command()

def vibration_off():
    command_bits["vibration"] = 0
    send_current_command()

# Universal STOP
def stop_all():
    command_bits.update({
        "motor_enable": 0,
        "drive_dir": "00",
        "plow_enable": 0,
        "plow_dir": 0,
        "vibration": 0
    })
    send_current_command()
