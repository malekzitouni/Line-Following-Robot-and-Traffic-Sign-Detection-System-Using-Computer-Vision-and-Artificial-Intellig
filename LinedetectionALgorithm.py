import cv2
import numpy as np
import time


def detectLine(frame):
    low_b = np.uint8([150, 150, 150])
    high_b = np.uint8([0, 0, 0])
    mask = cv2.inRange(frame, high_b, low_b)  # Create a binary mask to detect dark areas
    contours, _ = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)  # Find the contours
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)  # Draw contours on the original frame

    # Center of the frame
    center_x = frame.shape[1] // 2  # Horizontal center
    center_y = frame.shape[0] // 2  # Vertical center

    if len(contours) > 0:  # Check if there's at least one contour
        for contour in contours:  # Loop through the contours
            M = cv2.moments(contour)  # Calculate the moments for each contour
            if M['m00'] != 0:  # Ensure m00 is non-zero to avoid division by zero
                cx = int(M['m10'] / M['m00'])  # Compute x-coordinate of the centroid
                cy = int(M['m01'] / M['m00'])  # Compute y-coordinate of the centroid
                print("CX:" + str(cx) + " CY:" + str(cy))  # Print coordinates of the centroid
                print("Center_x:" + str(center_x) + " Center_y:" + str(center_y))  # Print coordinates of the centroid
                if cx < center_x and cy < center_y:
                    print('Right')
                elif cx > center_x and cy > center_y:
                    print('left')
                else:
                    print('Forward')

                # Mark the centroid with a circle
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    cv2.imshow('frame', frame)  # Display the frame
    cv2.imshow('mask', mask)  # Display the mask


def main():
    cv2.CAP_DSHOW = 700  # Windows-specific
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
  # Open the camera with ID 1
    cap.set(3, 640)  # Set frame width
    cap.set(4, 480)  # Set frame height
    while True:
        try:
            ret, frame = cap.read()  # Read a frame from the camera

            if ret:
                detectLine(frame)  # Detect lines in the frame

                time.sleep(0.006)  # Small delay

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key
                    break
        except Exception as e:
            print(f"Error: {e}")
            break

    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows


if __name__ == "__main__":
    main()
