import cv2
import numpy as np

# Source coordinates (points in the source image)
srcPoints = np.float32([
    [100, 200],  # Top-left
    [400, 200],  # Top-right
    [100, 400],  # Bottom-left
    [400, 400],  # Bottom-right
])

# Destination coordinates (points in the output image)
dstPoints = np.float32([
    [0, 0],       # Top-left
    [300, 0],     # Top-right
    [0, 300],     # Bottom-left
    [300, 300],   # Bottom-right
])

# Create the transformation matrix
perspective_transform_matrix = cv2.getPerspectiveTransform(srcPoints, dstPoints)

# Load an image
default_file = 'C:/Users/Pc/Desktop/WORK/line1.jpg.'
image = cv2.imread(default_file)

# Apply the perspective transformation to the image
output_image = cv2.warpPerspective(image, perspective_transform_matrix, (300, 300))

# Display the result
cv2.imshow("Transformed Image", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
