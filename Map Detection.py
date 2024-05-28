import sys
import cv2
import cv2 as cv
import numpy as np
import math

def main(argv):
    default_file = 'C:/Users/Pc/Desktop/WORK/line1.jpg.'
    filename = argv[0] if len(argv) > 0 else default_file

    # Load an image
    image = cv.imread(filename)
    roi = image[200:250, 0:639]
    Blackline = cv2.inRange(roi, (0,0,0), (10,10,10))
    kernel = np.ones((3,3), np.uint8)
    Blackline = cv2.erode(Blackline, kernel, iterations=5)
    Blackline = cv2.dilate(Blackline, kernel, iterations=9)
    contours, hierarchy = cv2.findContours(Blackline.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0 :
        x,y,w,h = cv2.boundingRect(contours[0])
        cv2.line(image, (int(x+(w/2)), 100), (int(x+(w/2)), 150), (0, 0, 255), 5)

    cv2.imshow("original with line", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])
