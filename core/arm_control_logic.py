# core/arm_control_logic.py

from hardware import arm, motors

def update_arm_state(context="clearing"):
    """
    Updates the arm and vibration state based on the current context.
    Contexts could include: 'clearing', 'reroute', 'pause', etc.
    """

    if context == "clearing":
        print("[ARM LOGIC] Lowering arm and enabling vibration.")

        arm.arm_down()
        motors.vibration_on()

        # if arm.is_arm_down() TODO: Add this function in 
        #     motors.vibration_on()
        # else:
        #     print("[ARM LOGIC] Arm not fully down. Skipping vibration.")

    elif context == "reroute":
        print("[ARM LOGIC] Raising arm and disabling vibration.")
        motors.vibration_off()
        arm.arm_up()

    elif context == "pause": # Pause is not implemented anywhere yet
        print("[ARM LOGIC] Pausing: stopping vibration and freezing arm.")
        motors.vibration_off()
        arm.stop_arm()

    else:
        print(f"[ARM LOGIC] Unknown context: {context}. No action taken.")
