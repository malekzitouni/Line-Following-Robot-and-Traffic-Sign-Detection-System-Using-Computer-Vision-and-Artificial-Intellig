import cv2
import time
from motors import Motor
import lanecurve
from picamera2 import Picamera2

# Constants for motor control
FORWARD_SPEED = 0.5
TURN_RATE = 0.3
SLEEP_TIME = 0.1  # Time to wait between updates

# Initialize motors (pin configuration might vary based on your setup)
motor = Motor(2, 3, 4, 17, 22, 27)

# Initialize the camera (adjust configuration if necessary)
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"  # 8 bits
picam2.start()

# Main loop
while True:
    # Read a frame from the camera
    img = picam2.capture_array()
    
    if img is None:
        print("Error: Failed to read frame from camera")
        break

    # Resize the image (if necessary)
    img = cv2.resize(img, (480, 240))

    # Get the lane curvature
    curve = lanecurve.getLaneCurve(img, display=0)  # Use 'display=2' to see the output
    print("Detected curve:", curve)

    # Determine steering based on curve
    if curve > 0.1:  # Turn right if curve is positive
        motor.move(FORWARD_SPEED, TURN_RATE, SLEEP_TIME)
    elif curve < -0.1:  # Turn left if curve is negative
        motor.move(FORWARD_SPEED, -TURN_RATE, SLEEP_TIME)
    else:  # Move forward if curve is near zero
        motor.move(FORWARD_SPEED, 0, SLEEP_TIME)

    # Add a small delay to avoid overloading the system
    time.sleep(0.05)

    # Break loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup and release resources
motor.stop()
picam2.stop()
cv2.destroyAllWindows()
