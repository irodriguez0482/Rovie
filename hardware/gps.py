# hardware/gps.py

import serial
import time
from utils.logger import log_gps

# Set up GPS serial communication
SERIAL_PORT = "/dev/gps_2"  # CHANGE IS NECCESSARY
BAUD_RATE = 9600

def parse_gps(nmea_sentence):
    """Extract latitude and longitude from a GGA or RMC sentence."""
    try:
        data = nmea_sentence.split(",")
        if data[0] == "$GPGGA" and data[2] and data[4]:
            lat = float(data[2]) / 100.0
            lon = float(data[4]) / 100.0
            return (lat, lon)
        elif data[0] == "$GPRMC" and data[3] and data[5]:
            lat = float(data[3]) / 100.0
            lon = float(data[5]) / 100.0
            return (lat, lon)
    except (ValueError, IndexError):
        pass
    return None

def GetCurrentLocation():
    """Returns the current (latitude, longitude) from GPS as floats, or (None, None) if invalid."""
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as gps_serial:
            gps_serial.flush()
            while True:
                line = gps_serial.readline().decode("utf-8", errors="ignore").strip()
                if line.startswith("$GPGGA") or line.startswith("$GPRMC"):
                    coords = parse_gps(line)
                    if coords:
                        log_gps(*coords)
                        return coords
    except serial.SerialException as e:
        print(f"[GPS ERROR] {e}")
    return (None, None)
