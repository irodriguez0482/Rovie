# mock/motors.py

from configs.test_scenarios import SCENARIO

print(f"[MAIN] Running SCENARIO: {SCENARIO['name']}")

current_command = {
    "motor_enable": 0,
    "drive_dir": "00",    # 00 = forward, 01 = back, 10 = left, 11 = right
    "plow_enable": 0,
    "plow_dir": 0,
    "vibration": 0
}

def init_serial():
    print("[MOCK MOTORS] Serial initialized (mocked).")

def cleanup():
    print("[MOCK MOTORS] Serial and GPIO cleaned up (mocked).")

def _send_mock_command():
    bits = (
        str(current_command["motor_enable"]) +
        current_command["drive_dir"] +
        str(current_command["plow_enable"]) +
        str(current_command["plow_dir"]) +
        str(current_command["vibration"])
    )
    print(f"[MOCK MOTORS] Sent command: {bits}")

# Drive movement
def drive_forward():
    current_command["motor_enable"] = 1
    current_command["drive_dir"] = "00"
    _send_mock_command()

def drive_backward():
    current_command["motor_enable"] = 1
    current_command["drive_dir"] = "01"
    _send_mock_command()

def turn_left():
    current_command["motor_enable"] = 1
    current_command["drive_dir"] = "10"
    _send_mock_command()

def turn_right():
    current_command["motor_enable"] = 1
    current_command["drive_dir"] = "11"
    _send_mock_command()

def stop_drive():
    current_command["motor_enable"] = 0
    _send_mock_command()

# Arm movement
def arm_up():
    current_command["plow_enable"] = 1
    current_command["plow_dir"] = 0
    _send_mock_command()

def arm_down():
    current_command["plow_enable"] = 1
    current_command["plow_dir"] = 1
    _send_mock_command()

def stop_arm():
    current_command["plow_enable"] = 0
    _send_mock_command()

# Vibration
def vibration_on():
    current_command["vibration"] = 1
    _send_mock_command()

def vibration_off():
    current_command["vibration"] = 0
    _send_mock_command()

# Full stop
def stop_all():
    current_command.update({
        "motor_enable": 0,
        "drive_dir": "00",
        "plow_enable": 0,
        "plow_dir": 0,
        "vibration": 0
    })
    _send_mock_command()
