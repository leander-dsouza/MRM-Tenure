import cv2
import numpy as np
from matplotlib import pyplot as plt



cap = cv2.VideoCapture(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5, 5))
kernel1= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3, 3))





while(1):

    # Take each frame
    _, frame = cap.read()


    # Convert BGR to HSV

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv=cv2.GaussianBlur(hsv,(5,5),0)

      # define range of yellow color in HSV
    lower_yellow = np.array([29,86,6])
    upper_yellow = np.array([64,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel1)


    mask = cv2.erode(mask,kernel,iterations=2)
    mask = cv2.dilate(mask,kernel1, iterations=13)

       # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame,  mask = mask)

# BOUNDING RECTANGLE .............................................................................................

    _, conts, hei = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts = np.array(conts)

    if len(conts) > 0:

        for i, contour in enumerate(conts):
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            aratio = (rect[1][0] / rect[1][1])
            if (aratio > 0.9) and (aratio < 1.1):
                cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)



            print("Aspect Ratio",aratio)



#HOUGH CIRCLES........................................................................................................



    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, param1=255, param2=20, minRadius=0, maxRadius=0)
    #     # print circles

    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle in the image
            # corresponding to the center of the circle

            if (aratio > 0.9) and (aratio < 1.1):
                cv2.circle(res, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(res, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                cv2.putText(frame,"BALL DETECTED",(x,y),cv2.FONT_HERSHEY_SIMPLEX,2,255)






#DISPLAY................................................................................................................



    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

#.....................................................................................................................
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
