#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu,MagneticField
from tf.transformations import euler_from_quaternion
import serial
from math import degrees

ser = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser.flushInput()

ob1 = Imu()
aligner = 360 - 0


def callback_imu():
    while True:
        serial_data = ser.readline()
        data = serial_data.split(',')
        if len(data)!= 10:
            continue
        
        ob1.orientation.x = float(data[0])
        ob1.orientation.y = float(data[1])
        ob1.orientation.z = float(data[2])
        ob1.orientation.w = float(data[3])

        orientation_list = [ob1.orientation.x, ob1.orientation.y, ob1.orientation.z, ob1.orientation.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

        yaw = degrees(yaw)
        if yaw < 0:
            yaw += 360

	yaw = (yaw +aligner)%360        
	print(360 - yaw)



callback_imu()



