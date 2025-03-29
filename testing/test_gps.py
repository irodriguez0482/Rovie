# tests/test_gps.py

import time
from hardware import gps

print("Testing GPS... Press Ctrl+C to stop.")

while True:
    lat, lon = gps.GetCurrentLocation()
    if lat is not None and lon is not None:
        print(f"Lat: {lat:.6f}, Lon: {lon:.6f}")
    else:
        print("Waiting for valid GPS signal...")
    time.sleep(1)
