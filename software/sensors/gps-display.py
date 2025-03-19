import mpu6050  # Library for MPU6050 IMU sensor (accelerometer & gyroscope)
import time  # Used for timekeeping
import serial  # Used to communicate with the GPS module
import csv  # Used to save data in CSV format
import os  # Used to check if the file exists

# Initialize MPU6050 (IMU Sensor) at I2C address 0x68
mpu = mpu6050.mpu6050(0x68)

# Define GPS Serial Port 
GPS_PORT = "/dev/ttyACM0"  # Change to "/dev/ttyACM1" if neccessary
BAUD_RATE = 9600  # Standard GPS baud rate
gps_serial = serial.Serial(GPS_PORT, BAUD_RATE, timeout=1)  # Open serial connection to GPS
# Define CSV file for logging data
LOG_FILE = "gps_imu_log.csv"

# Heading estimation variables
previous_time = time.time()  # Store the previous time for heading calculations
current_heading = 0  # Store estimated heading angle

# Function to read IMU data
def read_imu():
    """
    Reads accelerometer, gyroscope, and temperature from the MPU6050 sensor.
    Returns a dictionary with sensor values.
    """
    accel = mpu.get_accel_data()  # Read accelerometer data (X, Y, Z)
    gyro = mpu.get_gyro_data()  # Read gyroscope data (X, Y, Z)
    temp = mpu.get_temp()  # Read temperature data
    return {"accel": accel, "gyro": gyro, "temp": temp}

# Function to read raw GPS data
def read_gps():
    """
    Reads raw GPS data from the serial interface.
    Returns an NMEA sentence (GPGGA or GPRMC).
    """
    gps_serial.flush()  # Clear old data from the serial buffer
    while True:
        line = gps_serial.readline().decode("utf-8", errors="ignore").strip()  # Read and clean GPS data
        if line.startswith("$GPGGA") or line.startswith("$GPRMC"):  # Keep only useful GPS data
            return line  # Return the first valid GPS sentence found

# Function to parse GPS data (extract latitude & longitude)
def parse_gps(nmea_sentence):
    """
    Extracts latitude and longitude from a GPS NMEA sentence.
    Returns a dictionary with latitude and longitude.
    """
    try:
        data = nmea_sentence.split(",")  # Split the sentence by commas
        if data[0] == "$GPGGA":  # GPS fix data
            lat = float(data[2]) / 100.0
            lon = float(data[4]) / 100.0
            return {"latitude": lat, "longitude": lon}
        elif data[0] == "$GPRMC":  # Recommended minimum data
            lat = float(data[3]) / 100.0
            lon = float(data[5]) / 100.0
            return {"latitude": lat, "longitude": lon}
    except (ValueError, IndexError):
        return None  # Return None if parsing fails

# Function to estimate heading using gyroscope Z-axis (yaw)
def update_heading(gyro_z):
    """
    Uses the gyroscope Z-axis to estimate heading changes.
    This is a basic integration method and is prone to drift over time.
    """
    global previous_time, current_heading  # Use global variables
    current_time = time.time()  # Get current time
    dt = current_time - previous_time  # Calculate time difference
    previous_time = current_time  # Update previous time

    delta_angle = gyro_z * dt  # Compute heading change (°/s * seconds = degrees)
    current_heading += delta_angle  # Update estimated heading
    return current_heading  # Return updated heading estimate

# Function to initialize the CSV file with headers
def initialize_csv():
    """
    Creates the CSV file and writes the column headers if the file does not exist.
    """
    if not os.path.exists(LOG_FILE):  # Check if the CSV file exists
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp", "Accel_X", "Accel_Y", "Accel_Z",
                "Gyro_X", "Gyro_Y", "Gyro_Z", "Temperature",
                "GPS_Latitude", "GPS_Longitude", "Heading_Estimate"
            ])

# Function to log data into a CSV file
def log_data(entry):
    """
    Appends a new row of sensor data to the CSV file.
    """
    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(entry)

# Main function that continuously logs sensor data
def main():
    initialize_csv()  # Ensure CSV file exists with headers
    print("Logging GPS and IMU data... Press Ctrl+C to stop.")

    while True:
        try:
            # Read data from sensors
            imu_data = read_imu()  # Get IMU data (accelerometer, gyroscope, temp)
            gps_nmea = read_gps()  # Get raw GPS data
            gps_data = parse_gps(gps_nmea)  # Extract latitude & longitude

            # Estimate heading using gyro Z-axis
            estimated_heading = update_heading(imu_data["gyro"]["z"])

            # Prepare a list for logging
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
            log_entry = [
                timestamp,
                imu_data["accel"]["x"], imu_data["accel"]["y"], imu_data["accel"]["z"],
                imu_data["gyro"]["x"], imu_data["gyro"]["y"], imu_data["gyro"]["z"],
                imu_data["temp"],
                gps_data["latitude"] if gps_data else "N/A",
                gps_data["longitude"] if gps_data else "N/A",
                estimated_heading
            ]

            # Log the data into the CSV file
            log_data(log_entry)

            # Print data to the terminal for real-time monitoring
            print(f"{timestamp} | GPS: {gps_data} | Heading: {estimated_heading:.2f}°")

            time.sleep(1)  # Wait 1 second before reading again

        except KeyboardInterrupt:
            print("Logging stopped.")
            break  # Exit the loop when Ctrl+C is pressed

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
