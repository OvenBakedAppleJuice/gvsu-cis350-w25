import serial
import time

# Replace with the correct serial port for your Arduino
SERIAL_PORT = 'COM3'     # e.g., COM3 for Windows, /dev/ttyACM0 for Linux/Mac
BAUD_RATE = 9600         # Match this with your Arduino sketch

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino to reset
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

try:
    while True:
        user_input = input("Enter data to send (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
        ser.write((user_input + "\n").encode())  # Send data with newline
        print(f"Sent: {user_input}")
finally:
    ser.close()
    print("Serial connection closed.")
