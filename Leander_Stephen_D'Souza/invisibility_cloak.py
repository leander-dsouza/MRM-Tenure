import cv2
import numpy as np


cap = cv2.VideoCapture(0)


backdrop = 0

# CAPTURE 100 BACKGROUND INSTANCES
for i in range(100):
    _, backdrop = cap.read()
backdrop = np.flip(backdrop, axis=1)

# TRICK IS TO DILATE LIKE CRAZY
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11 , 11))
kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3, 3))


cv2.namedWindow('HSV palette')

def nothing(x):
    pass

cv2.createTrackbar('LH','HSV palette',0,179,nothing)
cv2.createTrackbar('LS','HSV palette',0,255,nothing)
cv2.createTrackbar('LV','HSV palette',0,255,nothing)

cv2.createTrackbar('UH','HSV palette',0,179,nothing)
cv2.createTrackbar('US','HSV palette',0,255,nothing)
cv2.createTrackbar('UV','HSV palette',0,255,nothing)




while True:

    _, frame = cap.read()

    frame = np.flip(frame, axis=1)
    og_frame = frame



    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)


    lh = cv2.getTrackbarPos('LH','HSV palette')
    ls = cv2.getTrackbarPos('LS', 'HSV palette')
    lv = cv2.getTrackbarPos('LV', 'HSV palette')

    uh = cv2.getTrackbarPos('UH', 'HSV palette')
    us = cv2.getTrackbarPos('US', 'HSV palette')
    uv = cv2.getTrackbarPos('UV', 'HSV palette')

    '''lower_maroon = np.array([lh, ls, lv])
    upper_maroon = np.array([uh, us, uv])'''

    lower_maroon = np.array([137, 84, 4])
    upper_maroon = np.array([179, 255, 255])
    og_mask = cv2.inRange(hsv, lower_maroon, upper_maroon)



    og_mask = cv2.morphologyEx(og_mask, cv2.MORPH_OPEN, kernel1)
    og_mask = cv2.morphologyEx(og_mask, cv2.MORPH_DILATE, kernel)


    inv_mask = cv2.bitwise_not(og_mask)

    no_cloak = cv2.bitwise_and(frame, frame, mask=inv_mask) # SUBTRACT CLOAK
    cloak = cv2.bitwise_and(backdrop, backdrop, mask=og_mask) # SUBTRACT EVERYTHING BUT CLOAK


    output = cv2.addWeighted(no_cloak, 1, cloak, 1, 0)

    og_mask = cv2.cvtColor(og_mask, cv2.COLOR_GRAY2BGR)
    inv_mask = cv2.cvtColor(inv_mask, cv2.COLOR_GRAY2BGR)

    horizontal1 = np.hstack([og_frame,og_mask])
    horizontal2 = np.hstack([inv_mask,output])
    vertical = np.vstack([horizontal1,horizontal2])


    cv2.putText(vertical, "ORIGINAL FRAME", (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.putText(vertical, "MASK", (650, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.putText(vertical, "INVERTED MASK", (10, 950), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.putText(vertical, "OUTPUT FRAME", (650, 950), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

    cv2.imshow('RESULTANT',vertical)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

