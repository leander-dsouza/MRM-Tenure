#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion



def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


pitch = 0.0
roll = 0.0
yaw = 0.0
aligner = 360 - 0

def callback_imu(msg):
    global heading,aligner

    orientation_list = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

    #print(yaw)
    if yaw>=0:
        heading = arduino_map(yaw, 0, 3.12, 0, 180)
        heading = (heading + aligner) % 360

    else:
        heading = arduino_map(yaw, -3.12, 0, 180, 360)
        heading = (heading + aligner) % 360

    print (heading)




def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.


    rospy.Subscriber("/imu_perfected", Imu, callback_imu)

    while not rospy.is_shutdown():
        rospy.sleep(0.01)

    # spin() simply keeps python from exiting until this node is stopped


if __name__ == '__main__':
    try:
        rospy.init_node('Communication', anonymous=True)
        #rate = rospy.Rate(50)  # 1hz

        listener()

    except rospy.ROSInterruptException:
        pass
