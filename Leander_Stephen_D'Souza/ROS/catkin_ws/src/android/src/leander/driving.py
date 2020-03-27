#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import String




f = open("lat_only.txt",'w')
g = open("lon_only.txt",'w')

lat1=0
lon1=0
sampling_GPS = -1
value = [None]*2

def callback_gps(msg):
    global lat1, lon1

    lat1 = msg.latitude
    lon1 = msg.longitude



def gps_sampler():
    global lat1, lon1,sampling_GPS

    if lat1==0 or lon1==0:
        return

    #sampling_GPS+=1


    f.write(str(lat1) + '\n')
    g.write(str(lon1) + '\n')


def callback_joy(msg):
    global value
    string = msg.data
    value = string.split()
    print(value)


def talk_listen():
    global value

    rospy.Subscriber("joystick_topic",String,callback_joy)
    rospy.Subscriber("/fix", NavSatFix, callback_gps)

    while not rospy.is_shutdown():
        if value[0]!='8000' and value[1]!='8000':
            gps_sampler()


        rate.sleep()

if __name__ == '__main__':
    try:

        rospy.init_node('talker', anonymous=True,disable_signals=True)
        rate = rospy.Rate(50)

        talk_listen()
    except rospy.ROSInterruptException:
        f.close()
        g.close()
