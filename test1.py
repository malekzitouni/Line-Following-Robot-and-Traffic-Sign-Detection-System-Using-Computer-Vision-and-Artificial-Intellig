import cv2 as cv
import numpy as np

# Read the input image
file = 'C:/Users/Pc/Desktop/WORK/line5.png'


# Load an image
src = cv.imread(file)

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv.Canny(gray, 50, 150, apertureSize=3)

# Detect lines using Hough Line Transform
lines = cv.HoughLines(edges, 1, np.pi / 180, 200)

# Get image dimensions
height, width = src.shape[:2]

# Create a blank canvas with the same dimensions as the input image
canvas = np.zeros((height, width, 3), dtype=np.uint8)

# Iterate through the detected lines
if lines is not None:
    for line in lines:
        rho, theta = line[0]

        # Compute intersection points with image boundaries
        x1 = int(rho * np.cos(theta))
        y1 = int(rho * np.sin(theta))
        x2 = int(x1 + 1000 * (-np.sin(theta)))  # Extend the line for visualization
        y2 = int(y1 + 1000 * (np.cos(theta)))

        # Filter line segments within image boundaries
        if 0 <= x1 < width and 0 <= x2 < width and 0 <= y1 < height and 0 <= y2 < height:
            cv.line(canvas, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the result
cv.imshow('Filtered Lines', canvas)
cv.waitKey(0)
cv.destroyAllWindows()
