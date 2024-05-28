import cv2
import numpy as np
from picamera2 import Picamera2
import utilities

curveList = []
avgVal = 10

def getLaneCurve(img, display=2):
    imgCopy = img.copy()
    imgResult = img.copy()
    
    #### STEP 1
    imgThres = utilities.thresholding(img)

    #### STEP 2
    hT, wT, c = img.shape
    points = utilities.valTrackbars()
    imgWarp = utilities.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = utilities.drawPoints(imgCopy, points)

    #### STEP 3
    middlePoint, imgHist = utilities.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHist = utilities.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint

    #### STEP 4
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))

    #### STEP 5
    if display != 0:
        imgInvWarp = utilities.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
      # Corrected lines using integer values for endpoints
cv2.line(imgResult, (int(wT // 2), int(midY)), (int(wT // 2 + (curve * 3)), int(midY)), (255, 0, 255), 5)
cv2.line(imgResult, (int(wT // 2 + (curve * 3)), int(midY - 25)), (int(wT // 2 + (curve * 3)), int(midY + 25)), (0, 255, 0), 5)
for x in range(-30, 30):
    w = wT // 20
    cv2.line(imgResult, (int(w * x + (curve // 50)), int(midY - 10)),
             (int(w * x + (curve // 50)), int(midY + 10)), (0, 0, 255), 2)


    if display == 2:
        imgStacked = utilities.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                                 [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Result', imgResult)

    #### NORMALIZATION
    curve = curve / 100
    if curve > 1: curve = 1
    if curve < -1: curve = -1

    return curve

if __name__ == '__main__':
    # Initialize the camera (adjust configuration if necessary)
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"  # 8 bits
    picam2.start()

    intialTrackBarVals = [102, 80, 20, 214]
    utilities.initializeTrackbars(intialTrackBarVals)
    frameCounter = 0

    while True:
        frameCounter += 1
        if frameCounter >= picam2.frames:
            frameCounter = 0

        img = picam2.capture_array()
        img = cv2.resize(img, (480, 240))
        curve = getLaneCurve(img, display=2)
        print(curve)
        print(curveList)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup and release resources
    cv2.destroyAllWindows()
    picam2.stop()
