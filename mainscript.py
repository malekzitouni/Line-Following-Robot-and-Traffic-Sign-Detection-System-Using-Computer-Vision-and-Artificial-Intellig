import cv2
import time
from  motors  import  Motor
import lanecurve

# Constants for motor control
FORWARD_SPEED = 0.5
TURN_RATE = 0.3
SLEEP_TIME = 0.1  # Time to wait between updates

# Initialize motors (pin configuration might vary based on your setup)
motor =  Motor(2, 3, 4, 17, 22, 27)

# Initialize the camera (adjust index if necessary)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Open default camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set desired frame width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set desired frame height

# Main loop
while True:
    # Read a frame from the camera
    success, img = cap.read()
    if not success:
        print("Error: Failed to read frame from camera")
        break

    # Resize the image (if necessary)
    img = cv2.resize(img, (480, 240))

    # Get the lane curvature
    curve = lanecurve.getLaneCurve(img, display=0)  # Use 'display=2' to see the output
    print("Detected curve:", curve)

    # Determine steering based on curve
    if curve > 0.1:  # Turn right if curve is positive::callmoveright
        Motor.move(FORWARD_SPEED, TURN_RATE, SLEEP_TIME)
    elif curve < -0.1:  # Turn left if curve is negative::callmoveleft
        Motor.move(FORWARD_SPEED, -TURN_RATE, SLEEP_TIME)
    else:  # Move forward if curve is near zero
        Motor.move(FORWARD_SPEED, 0, SLEEP_TIME)

    # Add a small delay to avoid overloading the system
    time.sleep(0.05)

    # Break loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup and release resources
Motor.stop()
cap.release()
cv2.destroyAllWindows()
