import  sys
import cv2 as cv
import cv2
import numpy as np
import math


def main(argv):
    default_file = 'C:/Users/Pc/Desktop/WORK/straight.png'
    filename = argv[0] if len(argv) > 0 else default_file

    # Load an image
    src = cv.imread(filename)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    low_b = np.uint8([5, 5, 5])
    high_b = np.uint8([0, 0, 0])
    mask = cv2.inRange(src, high_b, low_b)
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    # Thresholding
    th_val = 200  # Adjust threshold value as needed
    _, roi_img = cv2.threshold(gray, th_val, 255, cv2.THRESH_BINARY)

    # Inverting the image (negative image)
    roi_img = cv2.bitwise_not(roi_img)

    # Define structuring elements for erosion and dilation
    erode_elmt = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilate_elmt = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # Erosion
    roi_img = cv2.erode(roi_img, erode_elmt)

    # Dilation
    roi_img = cv2.dilate(roi_img, dilate_elmt)
    # Find contours in the ROI image
    #contours, hierarchy = cv2.findContours(roi_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Create an empty black image to draw contours on
    contour_image = np.zeros_like(roi_img)

    # Draw contours on the empty image
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 2)  # Draw all contours in white with thickness 2
    # Calculate image center
    image_center = (src.shape[1], src.shape[0])
  #  image_center = (roi_img.shape[1] , roi_img.shape[0] )
    print("center_x : " + str(roi_img.shape[1]) + "  center_y : " + str(roi_img.shape[0]))
    #cv2.circle(contour_image, (roi_img.shape[1], roi_img.shape[0]), 5, (255, 255, 0), -1)
    if len(contours) > 0 :
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            centroid_x = int(M["m10"] / M["m00"])
            centroid_y = int(M["m01"] / M["m00"])
            print("CX : "+str(centroid_x)+"  CY : "+str(centroid_y))

            # Compare centroid with image center
            if centroid_x < image_center[0] and centroid_y < image_center[1]:

                print("Turn right")
            elif centroid_x > image_center[0] and centroid_y > image_center[1]:
                print("Turn left")
            else:
                print("Move forward")
    # Display the ROI image
    cv2.imshow('ROI Image with Contours', contour_image)
    cv.imshow('ROI Image', roi_img)
    cv.imshow('Image', src)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return 0
if __name__ == "__main__":
        main(sys.argv[1:])