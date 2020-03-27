import socket
import cv2
from threading import Thread, Lock
import struct
import sys
import RPi.GPIO as GPIO
import time

debug = True
jpeg_quality = 30
host = '192.168.43.254'
port = 1080


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#DIRECTION PINS
ldir=5
rdir=23
#SPEED PINS

lspeed=13
rspeed=18


GPIO.setup(ldir, GPIO.OUT)
GPIO.setup(rdir,GPIO.OUT)
GPIO.setup(lspeed, GPIO.OUT)
GPIO.setup(rspeed,GPIO.OUT)


#frequency
p=GPIO.PWM(lspeed,100)
q=GPIO.PWM(rspeed,100)

p.start(0.00)
q.start(0.00)


def right():
    GPIO.output(ldir,True)
    GPIO.output(rdir,False)
    GPIO.output(lspeed,True)
    GPIO.output(rspeed,True)
    #p.ChangeDutyCycle(50)
    #q.ChangeDutyCycle(50)


def left():
    GPIO.output(ldir,False)
    GPIO.output(rdir,True)
    GPIO.output(lspeed,True)
    GPIO.output(rspeed,True)
    p.ChangeDutyCycle(30)
    q.ChangeDutyCycle(30)


def brutestop():
    GPIO.output(ldir, False)
    GPIO.output(rdir, True)
    GPIO.output(lspeed, False)
    GPIO.output(rspeed, False)


class VideoGrabber(Thread):
        def __init__(self, jpeg_quality):
            Thread.__init__(self)
            self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
            self.cap = cv2.VideoCapture(0)
            self.cap.set(3, 640)
            self.cap.set(4, 480)
            self.running = True
            self.buffer = None
            self.lock = Lock()

        def stop(self):
            self.running = False

        def get_buffer(self):

            if self.buffer is not None:
                    self.lock.acquire()
                    cpy = self.buffer.copy()
                    self.lock.release()
                    return cpy

        def run(self):
            while self.running:
                success, img = self.cap.read()
                if not success:
                        continue
                self.lock.acquire()
                result, self.buffer = cv2.imencode('.jpg', img, self.encode_param)
                self.lock.release()

grabber = VideoGrabber(jpeg_quality)
grabber.daemon = True
grabber.start()

running = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = (host, port)

print('starting up on %s port %s\n' % server_address)

sock.bind(server_address)
while running:
    #data_packed, address = sock.recvfrom(struct.calcsize('<L'))
    #data = struct.unpack('<L',data_packed)[0]
    left()
    (data1, addr) = sock.recvfrom(1024)

    #if(data == 1):

    if data1=='Hello!':
        print("BALL DETECTED")
        brutestop()
        GPIO.cleanup()

    buffer = grabber.get_buffer()
    if buffer is None:
            continue
    if len(buffer) > 65507:
        print ("too large sorry")
        sock.sendto(struct.pack('<L',struct.calcsize('<L')), addr)
        sock.sendto(struct.pack('L',404), addr) #capture error
        continue
    sock.sendto(struct.pack('<L',len(buffer)), addr)
    sock.sendto(buffer.tobytes(), addr)


print("Quitting..")
grabber.join()
sock.close()
sys.exit()
