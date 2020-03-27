import math
import smbus
import time
from gps3 import gps3
import numpy as np
import RPi.GPIO as GPIO
import time

#****************************************************************************************************************


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

dist=0
checkA=0
checkB=0
headA=0.0
headB=0.0
headC=0.0
headD=0.0

i=0
j=0

l=360-185
x_manual=1.5465
y_manual=1.4085

#left forward

trigPin1 = 27
echoPin1 = 17

# right forward

trigPin2 = 14
echoPin2 = 15

#left back

trigPin3 = 26
echoPin3 = 19

#right back

trigPin4 = 20
echoPin4 = 21

threshold = 30

GPIO.setup(trigPin1, GPIO.OUT)
GPIO.setup(echoPin1, GPIO.IN)

GPIO.setup(trigPin2, GPIO.OUT)
GPIO.setup(echoPin2, GPIO.IN)

GPIO.setup(trigPin3, GPIO.OUT)
GPIO.setup(echoPin3, GPIO.IN)

GPIO.setup(trigPin4, GPIO.OUT)
GPIO.setup(echoPin4, GPIO.IN)

#*********************************************************************************************************************

#DIRECTION PINS
ldir=9
rdir=23
#SPEED PINS

lspeed=11
rspeed=24


GPIO.setup(ldir, GPIO.OUT)
GPIO.setup(rdir,GPIO.OUT)
GPIO.setup(lspeed, GPIO.OUT)
GPIO.setup(rspeed,GPIO.OUT)


#frequency
p=GPIO.PWM(lspeed,100)
q=GPIO.PWM(rspeed,100)

p.start(0.00)
q.start(0.00)


#********************************************************************************************************************
t1 = 0.000000
t2 = 0.000000
t3 = 0.000000
t4 = 0.000000
t5 = 0.000000
t6 = 0.000000

tax1 = 0.000000
tax2 = 0.000000
tax3 = 0.000000
tax4 = 0.000000


#***************************************************************************************************************




min_x=0
max_x=0
min_y=0
max_y=0
min_z=0
max_z=0


t=0.0000

bus = smbus.SMBus(1)

def twos_complement(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

bus.write_byte_data(0x1E, 0x20, 0b01111100)
bus.write_byte_data(0x1E, 0x21, 0b00000000)
bus.write_byte_data(0x1E, 0x22, 0b00000000)
bus.write_byte_data(0x1E, 0x23, 0b00001100)


lat2 = 13.347906667
lon2 = 74.792238333
lat1 = 0.0000000
lon1 = 0.0000000

angle=0.0

x=0.00
y=0.00

def short_angle(x,y):
    if abs(x-y)<180.0:
        return (abs(x-y))

    else:
        return (360.0-abs(x-y))


#********************************************************************************************************************
def forward():
    GPIO.output(ldir,True)
    GPIO.output(rdir,True)
    GPIO.output(lspeed,True)
    GPIO.output(rspeed,True)
    #p.ChangeDutyCycle(50)
    #q.ChangeDutyCycle(50)


def backward():
    GPIO.output(ldir,False)
    GPIO.output(rdir,False)
    GPIO.output(lspeed,True)
    GPIO.output(rspeed,True)
    #p.ChangeDutyCycle(50)
    #q.ChangeDutyCycle(50)


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
    # p.ChangeDutyCycle(50)
    # q.ChangeDutyCycle(50)


def brutestop():
    GPIO.output(ldir, False)
    GPIO.output(rdir, True)
    GPIO.output(lspeed, False)
    GPIO.output(rspeed, False)

def backwardright():
    GPIO.output(ldir,False)
    GPIO.output(rdir,False)
    GPIO.output(lspeed,True)
    GPIO.output(rspeed,True)
    p.ChangeDutyCycle(100)
    q.ChangeDutyCycle(50)


def backwardleft():
    GPIO.output(ldir, False)
    GPIO.output(rdir, False)
    GPIO.output(lspeed, True)
    GPIO.output(rspeed, True)
    p.ChangeDutyCycle(50)
    q.ChangeDutyCycle(100)


def sideleftcheck():
    GPIO.output(trigPin3, True)
    time.sleep(10e-6)
    GPIO.output(trigPin3, False)

    while GPIO.input(echoPin3) == 0:
        pass

    t5 = time.time()

    while GPIO.input(echoPin3) == 1:
        t6 = time.time()
        tax3 = t6 - t5
        get = 0
        if tax3 > 0.005:
            get = 1
            break

    t6 = time.time()

    if get == 1:
        pass
        return 1

    duration3 = t6 - t5

    distance3 = duration3 * 17000

    if distance3 < threshold+10:
        print("ULTRASONIC OVERRIDE: FORWARD---")
        forward()
        p.ChangeDutyCycle(50)
        q.ChangeDutyCycle(50)

        return -1

def siderightcheck():
    GPIO.output(trigPin4, True)
    time.sleep(10e-6)
    GPIO.output(trigPin4, False)

    while GPIO.input(echoPin4) == 0:
        pass

    t7 = time.time()

    while GPIO.input(echoPin4) == 1:
        t8 = time.time()
        tax4 = t8 - t7
        put = 0
        if tax4 > 0.005:
            put = 2
            break

    t8 = time.time()

    if put == 2:
        pass
        return 1

    duration4 = t8 - t7

    distance4 = duration4 * 17000

    if distance4 < threshold+10:
        print("ULTRASONIC OVERRIDE: FORWARD---")
        forward()
        p.ChangeDutyCycle(50)
        q.ChangeDutyCycle(50)

        return -1


#.....................................................................................................................
def ultrasonic():
    while 1:

        time.sleep(0.1)
        GPIO.output(trigPin1, True)
        time.sleep(10e-6)
        GPIO.output(trigPin1, False)

        while GPIO.input(echoPin1) == 0:
            pass

        t1 = time.time()

        while GPIO.input(echoPin1) == 1:
            t2 = time.time()
            tax1 = t2 - t1
            i = 0
            if tax1 > 0.005:   #TIMEOUT AT 85cm
                i = 1
                break

        t2 = time.time()

        duration1 = t2 - t1

        distance1 = duration1 * 17000
        # .............................................
        GPIO.output(trigPin2, True)
        time.sleep(10e-6)
        GPIO.output(trigPin2, False)

        while GPIO.input(echoPin2) == 0:
            pass

        t3 = time.time()

        while GPIO.input(echoPin2) == 1:
            t4 = time.time()
            tax2 = t4 - t3
            j = 0
            if tax2 > 0.005:
                j = 2
                break

        t4 = time.time()

        #if (i + j) == 3:
         #   pass

        duration2 = t4 - t3

        distance2 = duration2 * 17000
#......................................................................................................................
#BACKWARD

        if (distance1 > threshold) and (distance2 > threshold):
            pass

        elif (distance1 < threshold+5) or (distance2 < threshold+5):
            backward()
            p.ChangeDutyCycle(50)
            q.ChangeDutyCycle(50)
            time.sleep(1)

            if distance1 < distance2:
                print("ULTRASONIC OVERRIDE: BACKWARD RIGHT")

                headC = np.round(roverheading(min_x, max_x, min_y, max_y, min_z, min_z))
                headD = headC

                while short_angle(headC, headD) < 90:
                    print("ULTRASONIC OVERRIDE: BACKWARD RIGHT")
                    right()
                    p.ChangeDutyCycle(50)
                    q.ChangeDutyCycle(50)
                    headD = np.round(roverheading(min_x, max_x, min_y, max_y, min_z, min_z))

                brutestop()
                checkB = sideleftcheck()

                while checkB == -1:
                    checkB = sideleftcheck()

                return -1

            else:
                print("ULTRASONIC OVERRIDE: BACKWARD LEFT")

                headA = np.round(roverheading(min_x, max_x, min_y, max_y, min_z, min_z))
                headB = headA

                while short_angle(headA, headB) < 90:
                    print("ULTRASONIC OVERRIDE: BACKWARD LEFT")
                    left()
                    p.ChangeDutyCycle(50)
                    q.ChangeDutyCycle(50)
                    headB = np.round(roverheading(min_x, max_x, min_y, max_y, min_z, min_z))

                brutestop()
                checkA = siderightcheck()

                while checkA == -1:
                    checkA = siderightcheck()

                return -1

            return -1

#LEFT90

        elif (distance2 < threshold) and (distance2 < distance1):
            print("ULTRASONIC OVERRIDE: LEFT90")

            headA = np.round(roverheading(min_x, max_x, min_y, max_y, min_z, min_z))
            headB=headA

            while short_angle(headA,headB) < 90:
                print("ULTRASONIC OVERRIDE: LEFT90")
                left()
                p.ChangeDutyCycle(50)
                q.ChangeDutyCycle(50)
                headB = np.round(roverheading(min_x, max_x, min_y, max_y, min_z, min_z))


            brutestop()
            checkA = siderightcheck()

            while checkA == -1:
                    checkA = siderightcheck()

            return -1
#.....................................................................................................................
# RIGHT90

        elif (distance1 < threshold) and (distance1 < distance2):
            print("ULTRASONIC OVERRIDE: RIGHT90")

            headC = np.round(roverheading(min_x, max_x, min_y, max_y, min_z, min_z))
            headD=headC

            while short_angle(headC,headD) < 90:
                print("ULTRASONIC OVERRIDE: RIGHT90")
                right()
                p.ChangeDutyCycle(50)
                q.ChangeDutyCycle(50)
                headD = np.round(roverheading(min_x, max_x, min_y, max_y, min_z, min_z))

            brutestop()
            checkB = sideleftcheck()

            while checkB == -1:
                checkB = sideleftcheck()

            return -1

        # SIDE ULTRASONICS..........................................................................................

        GPIO.output(trigPin3, True)
        time.sleep(10e-6)
        GPIO.output(trigPin3, False)

        while GPIO.input(echoPin3) == 0:
            pass

        t5 = time.time()

        while GPIO.input(echoPin3) == 1:
            t6 = time.time()
            tax3 = t6 - t5
            get = 0
            if tax3 > 0.005:
                get = 1
                break

        t6 = time.time()

        if get == 1:
            pass
            return 1

        duration3 = t6 - t5

        distance3 = duration3 * 17000

        if distance3 < threshold+10:
            print("ULTRASONIC OVERRIDE: FORWARD---")
            forward()
            p.ChangeDutyCycle(50)
            q.ChangeDutyCycle(50)

            return -1
        ##......................................................................................................

        GPIO.output(trigPin4, True)
        time.sleep(10e-6)
        GPIO.output(trigPin4, False)

        while GPIO.input(echoPin4) == 0:
            pass

        t7 = time.time()

        while GPIO.input(echoPin4) == 1:
            t8 = time.time()
            tax4 = t8 - t7
            put = 0
            if tax4 > 0.005:
                put = 2
                break

        t8 = time.time()

        if put == 2:
            pass
            return 1

        duration4 = t8 - t7

        distance4 = duration4 * 17000

        if distance4 < threshold:
            print("ULTRASONIC OVERRIDE: FORWARD---")
            forward()
            p.ChangeDutyCycle(50)
            q.ChangeDutyCycle(50)

            return -1


#......................................................................................................................

def haversine(lat1, lon1, lat2, lon2):
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
         math.cos(lat1) * math.cos(lat2))
    rad = 6378.1*1000
    c = 2 * math.asin(math.sqrt(a))
    dist= rad*c

    if dist < 7:
        print("GATE REACHED")
        quit()

    return dist

#......................................................................................................................
def bearing(lat1, lon1, lat2, lon2):
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) \
        - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)

    degree = math.atan2(y, x) * 180 / math.pi

    if degree < 0:
        degree += 360
    return degree
#....................................................................................................................
def roverheading(min_x,max_x,min_y,max_y,min_z,max_z):
    out_x_m_l = bus.read_byte_data(0x1E, 0x28)
    out_x_m_h = bus.read_byte_data(0x1E, 0x29)
    x = twos_complement((out_x_m_h << 8) | out_x_m_l, 16) / 1e3


    out_y_m_l = bus.read_byte_data(0x1E, 0x2A)
    out_y_m_h = bus.read_byte_data(0x1E, 0x2B)
    y = twos_complement((out_y_m_h << 8) | out_y_m_l, 16) / 1e3

    out_z_m_l = bus.read_byte_data(0x1E, 0x2C)
    out_z_m_h = bus.read_byte_data(0x1E, 0x2D)
    z = twos_complement((out_z_m_h << 8) | out_z_m_l, 16) / 1e3

    print("")

    if x < min_x:
        min_x = x
    if x > max_x:
        max_x = x

    if y < min_y:
        min_y = y
    if y > max_y:
        max_y = y

    if z < min_z:
        min_z = z
    if z > max_z:
        max_z = z

    offset_x = (max_x + min_x) / 2
    offset_y = (max_y + min_y) / 2
    offset_z = (max_z + min_z) / 2

    x = x - x_manual
    y = y - y_manual
    z = z - offset_z

    heading = math.atan2(y, x) * 180 / math.pi

    if heading < 0:
        heading += 360

    heading = (heading+l)% 360

    #print("HEADING=",heading)
    return heading

#....................................................................................................................

def displaydata(t,dist):

    if t < 10 and t > -10:
        print("STRAIGHT","DISTANCE=",dist)
        angle=0
        forward()
        p.ChangeDutyCycle(50)
        q.ChangeDutyCycle(50)
        #return

    elif t <= -180:
        angle=360+t
        print("ANTICLOCKWISE",angle,"DISTANCE=",dist)
        left()
        p.ChangeDutyCycle(30)
        q.ChangeDutyCycle(30)
        #return

    elif t < 0 and t > -180:
        angle=-t
        print("CLOCKWISE", angle,"DISTANCE=",dist)
        right()
        p.ChangeDutyCycle(30)
        q.ChangeDutyCycle(30)
        #return

    elif t >= 180:
        angle=360-t
        print("CLOCKWISE", angle,"DISTANCE=",dist)
        right()
        p.ChangeDutyCycle(30)
        q.ChangeDutyCycle(30)
        #return

    elif t > 0 and t < 180:
        angle=t
        print("ANTICLOCKWISE", angle,"DISTANCE=",dist)
        left()
        p.ChangeDutyCycle(30)
        q.ChangeDutyCycle(30)
        #return

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()





try:
 for new_data in gps_socket:
    v = ultrasonic()
    if v==1:
        pass
    else:
        continue

    if new_data:
            data_stream.unpack(new_data)
            lat1= data_stream.TPV['lat']
            lon1= data_stream.TPV['lon']
            if lat1 == 'n/a':
                continue
            if lon1 == 'n/a':
                continue

            dist=haversine(lat1, lon1, lat2, lon2)
            a = np.round(bearing(lat1, lon1, lat2, lon2))
            b = np.round(roverheading(min_x, max_x, min_y, max_y, min_z, min_z))
            t = b - a
    displaydata(t,dist)    #put in for

except KeyboardInterrupt:
    GPIO.cleanup()
