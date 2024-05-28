
import sys
import cv2
import cv2 as cv
import numpy as np
import math


# Load the image and convert it to grayscale
# Load the image and convert it to grayscale
def main(argv):
    default_file = 'C:/Users/Pc/Desktop/WORK/curve.png'
    filename = argv[0] if len(argv) > 0 else default_file

    # Load an image
    I = cv.imread(filename)
    im = cv.imread(filename, cv2.COLOR_BGR2GRAY)
    BW_THRESHOLD = 0.3
    MIN_CC_SIZE = 10
    VAR_THRESHOLD = 1
    SIMILAR_SIZE_THRESHOLD = 0.5
    MEDIAN_SIZE = 4

    # Initialize pipeMask
    pipeMask = None

    # Stage 1 - Thresholding and noise cleaning
    _, bwIm = cv2.threshold(im, BW_THRESHOLD * 255, 255, cv2.THRESH_BINARY)
    bwIm = cv2.fillPoly(bwIm, [np.array([[0, 0], [0, bwIm.shape[0]], [bwIm.shape[1], bwIm.shape[0]], [bwIm.shape[1], 0]], dtype=np.int32)], color=255)
    bwIm = cv2.morphologyEx(bwIm, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1)))

    # Connected Components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bwIm, connectivity=8)

    # Iterate over connected components
    for label in range(1, num_labels):
        if stats[label, cv2.CC_STAT_AREA] < MIN_CC_SIZE:
            continue

        ccMask = np.zeros_like(bwIm, dtype=np.uint8)
        ccMask[labels == label] = 255
        ccMaskEdges = cv2.Canny(ccMask, 100, 200)

        # Connected Components on edges
        num_labels2, labels2, stats2, centroids2 = cv2.connectedComponentsWithStats(ccMaskEdges, connectivity=5)
        if num_labels2 != 2:
            continue

        # Similar size test
        size1 = stats2[1, cv2.CC_STAT_AREA]
        size2 = stats2[2, cv2.CC_STAT_AREA]
        if min(size1, size2) / max(size1, size2) < SIMILAR_SIZE_THRESHOLD:
            continue

        # Masks
        topEdgeMask = np.zeros_like(ccMask, dtype=np.uint8)
        topEdgeMask[labels2 == 1] = 255
        bottomEdgeMask = np.zeros_like(ccMask, dtype=np.uint8)
        bottomEdgeMask[labels2 == 2] = 255

        # Variance of distances
        topEdgeDists = cv2.distanceTransform(topEdgeMask, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
        bottomEdgeDists = cv2.distanceTransform(bottomEdgeMask, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
        var1 = np.std(topEdgeDists[bottomEdgeMask.astype(bool)])
        var2 = np.std(bottomEdgeDists[topEdgeMask.astype(bool)])

        # Found pipe
        if var1 < VAR_THRESHOLD and var2 < VAR_THRESHOLD:
            pipeMask = ccMask
            break

        if topEdgeMask is not None:
            # Median Filtering
            topCorveY, topCurveX = np.nonzero(topEdgeMask)
            topCurveX = cv2.medianBlur(topCurveX.astype(np.float32), MEDIAN_SIZE).astype(np.uint8)
            topCurveY = cv2.medianBlur(topCorveY.astype(np.float32), MEDIAN_SIZE).astype(np.uint8)

# Display Results
        if pipeMask is not None:
          cv2.imshow('pipeMask', pipeMask)
          cv2.waitKey(0)
          cv2.destroyAllWindows()
        else:
          cv2.imshow('malek',I)
          print("ok")
if __name__ == "__main__":
    main(sys.argv[1:])
