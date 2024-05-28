import sys
import cv2 as cv
import numpy as np
import math

def main(argv):
    default_file = 'C:/Users/Pc/Desktop/WORK/roi.png'
    filename = argv[0] if len(argv) > 0 else default_file

    # Load an image
    src = cv.imread(filename)

    scale_percent = 100  # percent by which the image will be scaled
    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)
    srcr= cv.resize(src, (width, height), interpolation=cv.INTER_AREA)
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print('Usage: houghTransform.py [image_name -- default ' + default_file + '] \n')
        return -1
    dst = cv.Canny(srcr, 150, 230, None, 3)
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    lines = cv.HoughLines(dst, 1, np.pi / 180, 100, None, 0, 0)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv.line(cdst, pt1, pt2, (0, 0, 255), 1, cv.LINE_AA)

    # Apply Hough Circle Transform
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    circles = cv.HoughCircles(blurred, cv.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=10, maxRadius=100)

    # Ensure circles were detected
    if circles is not None:
        # Convert circle parameters to integers
        circles = np.uint16(np.around(circles))

        # Draw detected circles
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]
            cv.circle(cdst, center, radius, (0, 255, 0), 2)
    # Display the image in a window
    cv.imshow('Image', srcr)
    cv.imshow('Image1', dst)
    cv.imshow('Image2', cdst)

    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
    cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)
  # def line(img: cv2.typing.MatLike, pt1: cv2.typing.Point, pt2: cv2.typing.Point, color: cv2.typing.Scalar, thickness: int = ..., lineType: int = ..., shift: int = ...
    cv.imshow('Image5', cdst)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])


