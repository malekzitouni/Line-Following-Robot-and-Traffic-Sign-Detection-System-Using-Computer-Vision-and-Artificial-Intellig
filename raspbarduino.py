import serial  # Library to interact with serial ports
import time
import cv2
import lanecurve  # Custom module for lane curve detection
from motors import Motor  # Custom module for motor control

# Constants for motor control
FORWARD_SPEED = 0.5
TURN_RATE = 0.3
SLEEP_TIME = 0.1  # Time to wait between updates

# Open serial connection to the Arduino
arduino_port = '/dev/ttyACM0'  # Port may vary
baud_rate = 9600  # Ensure this matches the Arduino's baud rate

try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    print("Connected to Arduino")
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")
    exit(1)


# Open the camera to read frames
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Default camera, Windows-specific flag
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Main loop to read frames and control motors
while True:
    success, img = cap.read()  # Read a frame from the camera
    if not success:
        print("Error: Failed to read frame from camera")
        break

    # Get the lane curve
    curve = lanecurve.getLaneCurve(img, display=0)
    print("Detected curve:", curve)

    # Send command to Arduino based on the lane curve
    if curve > 0.1:  # Turn right
        arduino.write(b'R')  # Send 'R' for right turn
    elif curve < -0.1:  # Turn left
        arduino.write(b'L')  # Send 'L' for left turn
    else:  # Move forward
        arduino.write(b'F')  # Send 'F' for forward

    time.sleep(0.05)  # Wait before the next iteration

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit loop if 'q' is pressed
        break

# Stop motors and close resources
arduino.write(b'S')  # Send 'S' for stop
cap.release()
cv2.destroyAllWindows()
arduino.close()  # Close Arduino connection
