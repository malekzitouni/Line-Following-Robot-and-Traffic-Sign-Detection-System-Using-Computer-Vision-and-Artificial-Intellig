import cv2
import numpy as np
import utlis

# Initialize trackbars in a named window

def empty(a):
    pass
def initializeTrackbars(initial_trackbar_vals, wT=640, hT=480):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", initial_trackbar_vals[0], wT // 2, empty)
    cv2.createTrackbar("Height Top", "Trackbars", initial_trackbar_vals[1], hT, empty)
    cv2.createTrackbar("Width Bottom", "Trackbars", initial_trackbar_vals[2], wT // 2, empty)
    cv2.createTrackbar("Height Bottom", "Trackbars", initial_trackbar_vals[3], hT, empty)

# Get values from the trackbars and return the points
def valTrackbars(wT=640, hT=480):
    width_top = cv2.getTrackbarPos("Width Top", "Trackbars")
    height_top = cv2.getTrackbarPos("Height Top", "Trackbars")
    width_bottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    height_bottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([
        (width_top, height_top),
        (wT - width_top, height_top),
        (width_bottom, height_bottom),
        (wT - width_bottom, height_bottom),
    ])
    return points

# Warp the image based on given points
def warpImg(img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_warp = cv2.warpPerspective(img, matrix, (w, h))
    return img_warp

# Draw circles at the specified points
def drawPoints(img, points):
    for x in range(4):
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15, (0, 0, 255), cv2.FILLED)
    return img

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use the correct camera source
    cap.set(3, 640)  # Set frame width
    cap.set(4, 480)  # Set frame height

    # Initialize trackbars only once
    initial_trackbar_vals = [110, 208, 0, 480]
    initializeTrackbars(initial_trackbar_vals)

    while True:
        ret, img = cap.read()  # Check return value
        if not ret:
            print("Failed to capture frame")
            break

        img = cv2.resize(img, (640, 480))  # Resize the image
        img_thresh = utlis.thresholding(img)  # Ensure 'thresholding' function exists in 'utlis'

        # Get trackbar values and warp image
        points = valTrackbars()  # Get trackbar values
        img_warp = warpImg(img_thresh, points, 640, 480)  # Warp based on points

        # Draw points on the warped image
        img_warp_points = drawPoints(img_warp, points)  # Correct argument

        # Display the results - Initialize the windows only once
        cv2.imshow("frame_captured", img)
        cv2.imshow("thresholding", img_thresh)
        cv2.imshow("warpingimg", img_warp)
        cv2.imshow("warpingpoints", img_warp_points)

        # Exit loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release camera resources
    cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    main()

