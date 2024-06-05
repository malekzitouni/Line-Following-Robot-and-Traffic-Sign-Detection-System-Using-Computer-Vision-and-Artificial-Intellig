import cv2

# Set the preferred backend to DirectShow
cv2.CAP_DSHOW = 700  # Windows-specific

# Initialize video capture with the DirectShow backend
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam")
else:
    print("Webcam opened successfully")

# Set the desired frame size (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Adjust width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Adjust height

# Capture video frames in a loop
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not read frame")
        break

    # Display the frame in a window
    cv2.imshow('Webcam Video', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
