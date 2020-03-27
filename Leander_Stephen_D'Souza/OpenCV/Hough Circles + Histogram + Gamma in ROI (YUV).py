import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

count=0

def nothing(x):
    pass


# *********************************************************************************************************************
def adjust_gamma(image, gamma=1.0):
    if gamma == 0:
        gamma = 0.01

    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    return cv2.LUT(image, table)


# *********************************************************************************************************************

img = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow('GAMMA')

cv2.createTrackbar('g', 'GAMMA', 1, 200, nothing)

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file',
                    help='Path to video file (if not using camera)')
parser.add_argument('-c', '--color', type=str, default='color',
                    help='Color space: "color" (YUV)')
parser.add_argument('-b', '--bins', type=int, default=16,
                    help='Number of bins per channel (default 16)')
parser.add_argument('-w', '--width', type=int, default=0,

                    help='Resize video to specified width in pixels (maintains aspect)')
args = vars(parser.parse_args())

# Configure Videocap class instance for using camera or file input.
if not args.get('file', False):
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(args['file'])

color = args['color']
bins = args['bins']
resizeWidth = args['width']

# Initialize plot.
fig, ax = plt.subplots()

ax.set_title('Histogram (YUV)')

ax.set_xlabel('Bin = 256/16')
ax.set_ylabel('Frequency / 255')

# Initialize plot line object(s). Turn on interactive plotting and show plot.
lw = 3
alpha = 0.5

lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha, label='Y')
lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha, label='U')
lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha, label='V')

ax.set_xlim(0, bins - 1)
ax.set_ylim(0, 1)
ax.legend()
plt.ion()
plt.show()

# cap = cv2.VideoCapture(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

roi = cv2.imread(r'/home/leander/Desktop/dark.jpeg')

while (1):

    # Take each frame
    # _, frame = cap.read()
    (grabbed, frame) = cap.read()

    gamma = (cv2.getTrackbarPos('g', 'GAMMA')) * 0.05
    cv2.imshow('GAMMA', img)

    # gamma = 0.5 # change the value here to get different result
    frame = adjust_gamma(frame, gamma=gamma)

    if not grabbed:
        break

    # Convert BGR to HSV

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
    hsv = cv2.medianBlur(hsv ,3)

    # define range of yellow color in HSV
    lower_yellow = np.array([29, 86, 6])
    upper_yellow = np.array([64, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel1)

    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel1, iterations=13)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # BOUNDING RECTANGLE .............................................................................................

    _, conts, hei = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts = np.array(conts)

    if len(conts) > 0:

        for i, contour in enumerate(conts):
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            w = rect[1][0]
            h = rect[1][1]
            x1, y1, w1, h1 = cv2.boundingRect(contour)


            aratio = w / h  # width/height

            if (aratio > 0.9) and (aratio < 1.1):
                cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                w1 = 1 * w1
                h1 = 1 * h1
                frame_cut = hsv[int(y1): int(y1 + h1), int(x1): int(x1 + w1)]
                roi = cv2.cvtColor(frame_cut, cv2.COLOR_HSV2BGR)
                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2YUV)

                if roi is None or len(roi) == 0:
                    continue

# HOUGH CIRCLES........................................................................................................

                gray=cv2.cvtColor(frame_cut, cv2.COLOR_HSV2BGR)

                gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

                circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, param1=255, param2=20, minRadius=0,
                                           maxRadius=0)
                # print circles

                # ensure at least some circles were found
                if circles is not None:
                    # convert the (x, y) coordinates and radius of the circles to integers
                    circles = np.round(circles[0, :]).astype("int")
                    # loop over the (x, y) coordinates and radius of the circles
                    for (x, y, r) in circles:
                        # draw the circle in the output image, then draw a rectangle in the image
                        # corresponding to the center of the circle

                        if (aratio > 0.9) and (aratio < 1.1):
                            cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                            cv2.circle(frame, (x+x1, y+y1), r, (0, 255, 0), 4)
                            cv2.rectangle(frame, (x+x1 - 5, y+y1 - 5), (x+x1 + 5, y+y1 + 5), (0, 128, 255), -1)
                            cv2.putText(frame, "BALL DETECTED", (430, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0),
                                        3)

        # HISTOGRAM..........................................................................................................
        # Resize frame to width, if specified.
        if resizeWidth > 0:
            (height, width) = roi.shape[:2]
            resizeHeight = int(float(resizeWidth / width) * height)
            roi = cv2.resize(roi, (resizeWidth, resizeHeight),
                             interpolation=cv2.INTER_AREA)

        # Normalize histograms based on number of pixels per frame.
        numPixels = np.prod(roi.shape[:2])
        if roi is None or len(roi) == 0:
            continue

        print(roi)

        (y, u, v) = cv2.split(roi)

        cv2.imshow('roi', roi)

        histogramR = cv2.calcHist([y], [0], None, [bins], [0, 255]) / numPixels
        histogramG = cv2.calcHist([u], [0], None, [bins], [0, 255]) / numPixels
        histogramB = cv2.calcHist([v], [0], None, [bins], [0, 255]) / numPixels
        lineR.set_ydata(histogramR)
        lineG.set_ydata(histogramG)
        lineB.set_ydata(histogramB)

         fig.canvas.draw()

    # ....................................................................................................................


    # DISPLAY................................................................................................................

    cv2.putText(frame, "g={}".format(gamma), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)
    #cv2.imshow('res', res)
    # cv2.imshow('roi', roi)

    # .....................................................................................................................
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
