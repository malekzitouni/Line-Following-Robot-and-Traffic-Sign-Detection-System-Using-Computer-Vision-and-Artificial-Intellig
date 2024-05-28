import sys
import cv2
import numpy as np
import requests
def main(argv):
    cap = cv2.VideoCapture(1)
    '''if you get error instead of 1 try -1,2,3'''

    while True:
        try:
            # Read a frame from the video feed
            # Use HTTP instead of HTTPS
            ret, frame = cap.read()
            low_b = np.array([10, 10, 10])
            high_b = np.array([255, 255, 255])  # Adjusted the upper bound to white
            mask = cv2.inRange(frame, low_b, high_b)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame, contours, -2, (0, 0, 255), 2)

            cv2.imshow("Original with Contours", image)
            cv2.imshow("Mask", mask)
            # Exit the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                   break

        except Exception as e:
             print(f"Error: {e}")
             break

    cap.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main(sys.argv[1:])
