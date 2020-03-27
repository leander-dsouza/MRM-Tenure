#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu,MagneticField
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import NavSatFix
from math import *
import serial
from pyproj import Geod

wgs84_geod = Geod(ellps='WGS84')


def distance_bearing(lat1, lon1, lat2, lon2):
    global dist,degree
    degree,rev_degree,dist = wgs84_geod.inv(lon1, lat1, lon2, lat2)
    if degree < 0:
        degree += 360


pitch = 0.0
roll = 0.0
yaw = 0.0

f = open("lat_only.txt", "r")
g = open("lon_only.txt", "r")

ser = serial.Serial(
    port='/dev/ttySTM',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


def forward():
    global gear
    print('FORWARD')
    joystick_encoder(8000, 16000, gear)


def backward():
    global gear
    print('BACKWARD')
    joystick_encoder(8000, 0, gear)


def right():
    global gear
    print("RIGHT")
    joystick_encoder(16000, 8000, gear)


def left():
    global gear
    print("LEFT")
    joystick_encoder(0, 8000, gear)


def brutestop():
    global gear
    print("BRUTESTOP")
    joystick_encoder(8000, 8000, gear)


def joystick_encoder(x_joy, y_joy, gear):
    gear_pack = (0b00001111 & gear)

    x1 = 0b00001111 & (x_joy >> 10)
    x1 |= 0b00100000

    x2 = 0b000011111 & (x_joy >> 5)
    x2 |= 0b01000000

    x3 = 0b00000000011111 & (x_joy >> 0)
    x3 |= 0b01100000

    y1 = 0b00001111 & (y_joy >> 10)
    y1 |= 0b10000000

    y2 = 0b000011111 & (y_joy >> 5)
    y2 |= 0b10100000

    y3 = 0b00000000011111 & (y_joy >> 0)
    y3 |= 0b11000000

    ser.write('m')
    ser.write(chr(gear_pack))
    ser.write(chr(x1))
    ser.write(chr(x2))
    ser.write(chr(x3))
    ser.write(chr(y1))
    ser.write(chr(y2))
    ser.write(chr(y3))


gear = 2
heading = 0
degree = 0
dist = 10
lat1 = 0
lon1 = 0
dist_buffer = 1.5
angle_buffer = 15.0


aligner = 360 - 0


def callback_imu(msg):
    global heading, aligner

    orientation_list = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

    yaw = degrees(yaw)
    if yaw < 0:
        yaw += 360
    yaw = (yaw+aligner)%360

    heading = 360 -yaw



def callback_gps(msg):
    global lat1, lon1

    lat1 = msg.latitude
    lon1 = msg.longitude

  

def displaydata(t, dist):
    global angle_buffer

    if (angle_buffer/2) > t > -(angle_buffer/2):
        print("STRAIGHT", "DISTANCE=", dist)
        forward()

    elif t <= -180:
        angle = 360 + t
        print("ANTICLOCKWISE", angle, "DISTANCE=", dist)
        left()

    elif 0 > t > -180:
        angle = -t
        print("CLOCKWISE", angle, "DISTANCE=", dist)
        right()


    elif t >= 180:
        angle = 360 - t
        print("CLOCKWISE", angle, "DISTANCE=", dist)
        right()

    elif 0 < t < 180:
        angle = t
        print("ANTICLOCKWISE", angle, "DISTANCE=", dist)
        left()


def listener():
    global dist,lat1,lon1,dist_buffer
    rospy.Subscriber("/imu_data/raw", Imu, callback_imu)
    rospy.Subscriber("/fix", NavSatFix, callback_gps)

    while not rospy.is_shutdown():

        rospy.sleep(0.01)

        f1 = f.readlines()
        g1 = g.readlines()

        for latitude, longitude in zip(f1, g1):
            lat2 = float(latitude)
            lon2 = float(longitude)

            while dist > dist_buffer:
                distance_bearing(lat1, lon1, lat2, lon2)
                t = heading - degree
                displaydata(t, dist)

            print("WAYPOINT REACHED")
            dist = 10
            continue

        print("GOAL REACHED")
        brutestop()
        break


if __name__ == '__main__':
    try:
        global ob1
        rospy.init_node('Communication', anonymous=True,disable_signals=True)
        rate = rospy.Rate(50)  # 1hz

        listener()

    except rospy.ROSInterruptException:
        pass
