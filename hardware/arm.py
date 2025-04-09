# hardware/arm.py

from hardware import motors

def arm_up():
    """Raises the arm and waits for Arduino confirmation."""
    print("[ARM] Sending arm up command...")
    motors._send_to_arduino("000100")  # Enable plow + up

def arm_down():
    """Lowers the arm and waits for Arduino confirmation."""
    print("[ARM] Sending arm down command...")
    motors._send_to_arduino("000110")  # Enable plow + down

def stop_arm():
    """Stops the arm motor."""
    motors._send_to_arduino("000000")  # Universal stop
    
def is_arm_down():
    """Return True if arm is assumed to be fully down."""
    # Right now, we rely on Arduino sending 'ArduinoReady' after lowering
    print("[ARM] is_arm_down() → True (assumed)")
    return True

def is_arm_up():
    """Return True if arm is assumed to be fully up."""
    print("[ARM] is_arm_up() → True (assumed)")
    return True
