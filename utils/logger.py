# utils/logger.py

import os
import csv
import time
from datetime import datetime

LOG_BASE_PATH = "logs/gps/"

def ensure_log_dir():
    """Creates log directory if it doesn't exist."""
    os.makedirs(LOG_BASE_PATH, exist_ok=True)

def log_gps(latitude, longitude):
    """Logs GPS coordinates to a CSV file with timestamp."""
    ensure_log_dir()
    filename = os.path.join(LOG_BASE_PATH, f"gps_log_{datetime.now().strftime('%Y-%m-%d')}.csv")
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, latitude, longitude])

def log_flagged_gps(lat, lon, note=""):
    """Logs flagged GPS coordinates to a file with optional note."""
    path = "logs/flags/"
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, "flagged_gps_log.csv")

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, lat, lon, note])