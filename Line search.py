import cv2
import numpy as np
import time
import utlis


def getLaneCurve(img):
    img_thresh = utlis.thresholding(img)
    cv2.imshow('thresh', img_thresh)
    return None


def main():
    cv2.CAP_DSHOW = 700  # Windows-specific

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


    cap.set(3, 640)  # Set frame width
    cap.set(4, 480)  # Set frame height

    while True:
        try:
            ret, frame = cap.read()  # Read a frame from the camera
            if not ret:
                print("Failed to capture frame")
                break




            getLaneCurve(frame)  # Process frame for lane curve detection

            cv2.imshow('Video', frame)  # Show the captured video

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit loop on 'q'
                break

            time.sleep(0.006)  # Small delay to avoid high CPU usage

        except Exception as e:
            print(f"Error: {e}")
            break

    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows


if __name__ == "__main__":
    main()
