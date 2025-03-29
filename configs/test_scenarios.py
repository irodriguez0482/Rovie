# test_scenarios.py

# Time (in seconds) since start of test run when events should occur
SCENARIO = {
    "name": "Multiple obstacles and E-Stop",

    "force_button_press_times": [
        5,   # First obstacle
        10,  # Second obstacle
        15,  # Third obstacle
    ],

    "estop_trigger_time": 18,  # Simulated emergency shutdown

    "gps_fail_times": [7, 14],  # GPS drops out for a moment at these seconds

}
