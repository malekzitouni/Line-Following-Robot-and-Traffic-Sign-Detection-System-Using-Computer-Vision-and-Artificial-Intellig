import cv2

# Check available cameras
index = 0
arr = []
while index < 10:  # Check the first 10 possible indexes
    cap = cv2.VideoCapture(index)
    if cap.read()[0]:  # If a camera is found
        arr.append(index)
    cap.release()
    index += 1

print("Available camera indexes:", arr)
import cv2

camera_indexes = [1, 2, 3]

for index in camera_indexes:
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Camera {index} could not be opened")
    else:
        ret, frame = cap.read()
        if ret:
            cv2.imshow(f"Camera {index}", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print(f"Camera {index} opened but could not read a frame")
    cap.release()
