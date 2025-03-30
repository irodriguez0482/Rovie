# config/test_scenarios.py

SCENARIOS = {
    "default": {
        "name": "Default clean run",
        "force_button_press_times": [],
        "estop_trigger_time": None,
        "gps_fail_times": []
    },
    "obstacle_map_test": {
        "name": "Map Grid Test",
        "force_button_press_times": [4, 10],
        "estop_trigger_time": None,
        "gps_fail_times": []
    },
    "estop_midway": {
        "name": "Emergency Stop Test",
        "force_button_press_times": [],
        "estop_trigger_time": 12,
        "gps_fail_times": []
    },
    "gps_dropouts": {
        "name": "GPS Signal Drop Test",
        "force_button_press_times": [],
        "estop_trigger_time": None,
        "gps_fail_times": [5, 15]
    }
}

# Choose the active one here:
ACTIVE_SCENARIO_NAME = "obstacle_map_test"
SCENARIO = SCENARIOS[ACTIVE_SCENARIO_NAME]
