# main.py

import argparse
import sys

# ========== CLI PARSER ==========
def parse_args():
    parser = argparse.ArgumentParser(description="Run the rover system.")
    parser.add_argument("--mock", action="store_true", help="Run with mock hardware (simulation mode)")
    parser.add_argument("--hardware", action="store_true", help="Run with real hardware")
    return parser.parse_args()

args = parse_args()

if args.mock and args.hardware:
    print("[ERROR] Choose only one: --mock or --hardware")
    sys.exit(1)

USE_MOCK = args.mock or not args.hardware  # Default to mock

# ========== CONDITIONAL HARDWARE MODULE SETUP ==========
if USE_MOCK:
    print("[MAIN] Running in MOCK mode.")
    import hardware.mock.gps as gps
    import hardware.mock.motors as motors
    import hardware.mock.force_button as force_button
    import hardware.mock.arm as arm
    import hardware.mock.estop as estop
    import hardware.mock.start_button as start_button
else:
    print("[MAIN] Running in HARDWARE mode.")
    import hardware.mock.gps as gps
    import hardware.mock.motors as motors
    import hardware.mock.force_button as force_button
    import hardware.mock.arm as arm
    import hardware.mock.estop as estop
    import hardware.mock.start_button as start_button

# Inject selected hardware modules into sys.modules so all core code uses them
import types
sys.modules["hardware.gps"] = gps
sys.modules["hardware.motors"] = motors
sys.modules["hardware.force_button"] = force_button
sys.modules["hardware.arm"] = arm
sys.modules["hardware.estop"] = estop

# Now safely import core modules
import core.autonomous as autonomous

# ========== MAIN ENTRY POINT ==========
def main():
    print("[MAIN] Starting autonomous routine...")
    autonomous.run_autonomous_mode()
    print("[MAIN] Shutdown complete.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[MAIN] Shutdown via KeyboardInterrupt.")
    finally:
        motors.cleanup()
        force_button.cleanup()
        estop.cleanup()
        start_button.cleanup()
