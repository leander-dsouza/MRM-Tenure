import cv2
import numpy as np
from matplotlib import pyplot as plt








#........................................LEFT...................................................................
mtxL = [[712.86380503, 0.         , 275.59994691],
       [0.          , 707.8276494, 208.89880305],
       [0.          , 0.         , 1.]]

mtxL = np.array(mtxL)
mtxL = mtxL.reshape(3,3)

distL = np.array([[ 0.14351222, -1.57339319, -0.00878693, -0.01774397,  4.13629383]])
distL = distL.reshape(1,5)
print("Left distortion Matrix =\n",distL)
print("Left Camera Matrix =\n",mtxL)
#...............................................RIGHT.........................................................
mtxR = [[711.94365243, 0.          , 295.13498024],
       [0.          , 710.40877319, 246.79039608],
       [0.          , 0.          , 1.]]

mtxR = np.array(mtxR)
mtxR = mtxR.reshape(3,3)

distR = np.array([[ -0.03520351, -0.02070814, 0.00387548, -0.00933771,  -0.47234004]])
distR = distR.reshape(1,5)
print("Right Distortion Matrix =\n",distR)
print("Right Camera Matrix =\n",mtxR)




capL = cv2.VideoCapture(0)
capR = cv2.VideoCapture(1)





while True:
    # Capture frame-by-frame
    retL, frameL = capL.read()
    retR, frameR = capR.read()

    #frameL = cv2.GaussianBlur(frameL, (5, 5), 0)
    #frameL = cv2.medianBlur(frameL, 3)
    frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
    frameL = cv2.resize(frameL, (640, 480))
    hL, wL = frameL.shape[:2]

    # Generate new camera matrix from parameters
    newcameramatrixL, roiL = cv2.getOptimalNewCameraMatrix(mtxL, distL, (wL, hL), 0)

    # Generate look-up tables for remapping the camera image
    mapxL, mapyL = cv2.initUndistortRectifyMap(mtxL, distL, None, newcameramatrixL, (wL, hL), 5)

    # Remap the original image to a new image
    frameL = cv2.remap(frameL, mapxL, mapyL, cv2.INTER_LINEAR)
    cv2.imshow("LEFT",frameL)

    #frameR = cv2.GaussianBlur(frameR, (5, 5), 0)
    #frameR = cv2.medianBlur(frameR, 3)
    frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)
    frameR = cv2.resize(frameR, (640, 480))
    hR, wR = frameL.shape[:2]

    # Generate new camera matrix from parameters
    newcameramatrixR, roiR = cv2.getOptimalNewCameraMatrix(mtxR, distR, (wR, hR), 0)

    # Generate look-up tables for remapping the camera image
    mapxR, mapyR = cv2.initUndistortRectifyMap(mtxR, distR, None, newcameramatrixR, (wR, hR), 5)

    # Remap the original image to a new image
    frameR = cv2.remap(frameR, mapxR, mapyR, cv2.INTER_LINEAR)
    cv2.imshow("RIGHT",frameR)

    window_size = 5
    min_disp = 16
    num_disp = 192 - min_disp
    blockSize = window_size
    uniquenessRatio = 1
    speckleRange = 3
    speckleWindowSize = 3
    disp12MaxDiff = 200
    P1 = 600
    P2 = 2400
    imgL = frameR  #BACK VIEW
    imgR = frameL
    stereo = cv2.StereoSGBM_create(
        minDisparity=16,
        numDisparities=num_disp,
        blockSize=window_size,
        uniquenessRatio=uniquenessRatio,
        speckleRange=speckleRange,
        speckleWindowSize=speckleWindowSize,
        disp12MaxDiff=disp12MaxDiff,
        P1=P1,
        P2=P2
    )
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    cv2.imshow('disparity', (disp - min_disp) / num_disp)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
capL.release()
capR.release()
cv2.destroyAllWindows()
