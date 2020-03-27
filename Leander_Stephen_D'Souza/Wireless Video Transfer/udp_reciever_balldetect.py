import socket
import cv2
import numpy as np
import struct
from threading import Thread, Lock



kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5, 5))
kernel1= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3, 3))






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
                    print "byte recv: ", data_len
                try:
                    data, server = self.sock.recvfrom(data_len)
                except socket.timeout:
                    continue
                except Exception:
                    continue
                if not len(data) == data_len:
                    print "There was a image packet loss..."
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





if __name__ == '__main__':
    image = ImageGrabber('192.168.43.154', 1080)
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
                
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

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
                        aratio = (rect[1][0] / rect[1][1])
                        if (aratio > 0.9) and (aratio < 1.1):
                            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

                        print("Aspect Ratio", aratio)

                # HOUGH CIRCLES........................................................................................................

                gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

                circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, param1=255, param2=20, minRadius=0,
                                           maxRadius=0)
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
                            cv2.putText(frame, "BALL DETECTED", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

                # DISPLAY................................................................................................................

                cv2.imshow('frame', frame)
                cv2.imshow('mask', mask)
                cv2.imshow('res', res)

                # .....................................................................................................................
                k = cv2.waitKey(5) & 0xFF
                if k == 27:
                    break

#----------------------------------------------------------------------------------------------------------------------

            except Exception:
                continue
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        image.stopServer()
        image.sock.close()
