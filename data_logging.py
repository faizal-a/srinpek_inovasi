import serial
import csv
import time

# Serial port configuration
SERIAL_PORT = 'COM3'  # Update this with your serial port
BAUD_RATE = 9600

# Open the serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  # Wait for the serial connection to initialize

# Create a CSV file and write headers
with open('hydroponics_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Soil Moisture', 'Water Level', 'Temperature (C)', 'Humidity (%)'])

    try:
        while True:
            # Read a line from the serial port
            line = ser.readline().decode('utf-8').strip()
            # Print the line for debugging
            print(line)

            # Parse the line if it contains the sensor values
            if "Soil Moisture:" in line and "Water Level:" in line and "Humidity:" in line and "Temperature:" in line:
                # Extract the sensor values from the line
                parts = line.split("\t")
                soil_moisture = parts[0].split(": ")[1]
                water_level = parts[1].split(": ")[1]
                humidity = parts[2].split(": ")[1].replace("%", "")
                temperature = parts[3].split(": ")[1].replace("C", "")

                # Get the current timestamp
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                # Write the data to the CSV file
                writer.writerow([timestamp, soil_moisture, water_level, temperature, humidity])
                print(f"Logged data: {timestamp}, {soil_moisture}, {water_level}, {temperature}, {humidity}")

    except KeyboardInterrupt:
        print("Logging stopped by user")

    finally:
        ser.close()
