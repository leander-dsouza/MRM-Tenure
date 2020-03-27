#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
import serial
from tf.transformations import euler_from_quaternion
from math import degrees

ser = serial.Serial(
    port='/dev/ttyIMU',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser.flushInput()

ob1 = Imu()

ob1.header.frame_id = 'imu'
ob1.orientation_covariance = [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]



def callback_imu():
    while True:
        serial_data = ser.readline()
        data = serial_data.split(',')
        if len(data) !=10:
            continue


        ob1.orientation.x = float(data[0])
        ob1.orientation.y = float(data[1])
        ob1.orientation.z = float(data[2])
        ob1.orientation.w = float(data[3])



        ob1.linear_acceleration.x = float(data[4])
        ob1.linear_acceleration.y = float(data[5])
        ob1.linear_acceleration.z = float(data[6])

        ob1.angular_velocity.x = float(data[7])
        ob1.angular_velocity.y = float(data[8])
        ob1.angular_velocity.z = float(data[9])

        pub_i.publish(ob1)

if __name__ == '__main__':
    try:
        rospy.init_node('bno080_lsm9ds1_publisher', anonymous=True,disable_signals=True)
        pub_i = rospy.Publisher('imu_data/raw', Imu, queue_size=10)
        rate = rospy.Rate(50)  # 1hz

        callback_imu()

    except rospy.ROSInterruptException:
        pass

