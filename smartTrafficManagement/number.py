import serial
import time

# Adjust the serial port as needed (e.g., '/dev/ttyACM0' for Linux or 'COM3' for Windows)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Allow time for the serial connection to initialize

filename = "carsCount.txt"

while True:
    try:
        with open(filename, "r") as file:
            data = file.read().strip()  # Read the latest counts from the file

        if data:
            print("Sending:", data)

            # Clear serial buffers before sending new data
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            ser.write((data + "\n").encode('utf-8'))  # Send latest count

            # **Wait for Arduino acknowledgment**
            while True:
                response = ser.readline().decode('utf-8').strip()
                if response == "DONE":  # Adjust this based on Arduino response
                    print("Arduino completed operation. Sending new data...")
                    break  # Proceed with sending the next update
        
        else:
            print("File is empty!")
    
    except Exception as e:
        print("Error reading file:", e)

    # Delay before checking the file again
    time.sleep(1)  # Shorter delay, as we are waiting for Arduino
