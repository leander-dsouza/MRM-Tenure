import socket
import cv2
import numpy as np
import struct
from threading import Thread, Lock
import argparse
import sys
from matplotlib import pyplot as plt
import time

count=0


def goto(linenum):
    global line
    line = linenum


SERVER_IP   = '192.168.43.180'
PORT_NUMBER = 1080




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

img1= np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow('GAMMA')

cv2.createTrackbar('g', 'GAMMA', 80, 200, nothing)



# cap = cv2.VideoCapture(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))









class ImageGrabber(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.lock = Lock()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (host, port)
        self.sock.settimeout(0.2)
        self.array = None
        self.running = True

    def stopServer(self):
        self.sock.sendto(struct.pack('<L',0), self.server_address)

    def imageGrabber(self):
        if self.array is not None:
            self.lock.acquire()
            array = self.array
            self.lock.release()
            return array

    def run(self):
        while self.running:
            try:
                self.sock.sendto(struct.pack('<L',1), self.server_address)
                try:
                    data_len_packed, server = self.sock.recvfrom(struct.calcsize('<L'))
                except socket.timeout:
                    continue
                data_len = struct.unpack('<L',data_len_packed)[0]
                if data_len < 65507:
                    print ("byte recv: ", data_len)
                try:
                    data, server = self.sock.recvfrom(data_len)
                except socket.timeout:
                    continue
                except Exception:
                    continue
                if not len(data) == data_len:
                    print ("There was a image packet loss...")
                    continue
                if data == 404:
                    continue
                self.lock.acquire()
                self.array = np.frombuffer(data, dtype=np.dtype('uint8'))
                self.lock.release()

            except:
                self.running = False
                self.lock.acquire()
                self.image = None
                self.lock.release()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
myMessage = "Hello!"


if __name__ == '__main__':
    image = ImageGrabber('192.168.43.180', 1080)
    image.daemon = True
    image.start()
    try:
        while image.running:
            array = image.imageGrabber()
            if array is None:
                continue
            frame = cv2.imdecode(array, 1)
            ## Do some Processing here


            #
            #
            #
            try:

                gamma = (cv2.getTrackbarPos('g', 'GAMMA')) * 0.05
                cv2.imshow('GAMMA', img1)
                frame = adjust_gamma(frame, gamma=gamma)

                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
                hsv = cv2.medianBlur(hsv, 3)

                # define range of yellow color in HSV
                lower_yellow = np.array([29, 60, 20])  # mine 29 86 6
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

                            gray = cv2.cvtColor(frame_cut, cv2.COLOR_HSV2BGR)

                            gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

                            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, param1=255, param2=20,
                                                       minRadius=0,
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
                                        cv2.circle(frame, (x + x1, y + y1), r, (0, 255, 0), 4)
                                        cv2.rectangle(frame, (x + x1 - 5, y + y1 - 5), (x + x1 + 5, y + y1 + 5),
                                                      (0, 128, 255), -1)
                                        cv2.putText(frame, "BALL DETECTED", (430, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                                    (255, 0, 0),
                                                    3)
                                        sock.sendto(myMessage.encode('utf-8'), (SERVER_IP, PORT_NUMBER))
                                        frame=cv2.imread(r'/home/leander/Desktop/dark.jpeg')
                                        goto(117)

                                       

                # ....................................................................................................................

                # DISPLAY................................................................................................................

                cv2.putText(frame, "g={}".format(gamma), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                cv2.imshow('frame', frame)
                # cv2.imshow('mask', mask)
                # cv2.imshow('res', res)
                # cv2.imshow('roi', roi)

                # .....................................................................................................................
                k = cv2.waitKey(5) & 0xFF
                if k == 27:
                    break



            except Exception:
                continue
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        image.stopServer()
        image.sock.close()
        sys.exit()
