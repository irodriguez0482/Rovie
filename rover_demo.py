elif keyboard.is_pressed('v'):
    print("[DEMO] Vibration ON (1s pulse)")
    motors.vibration_on()
    time.sleep(1)
    motors.vibration_off()
    print("[DEMO] Vibration OFF (auto)")
    time.sleep(0.5)  # To avoid accidental re-trigger