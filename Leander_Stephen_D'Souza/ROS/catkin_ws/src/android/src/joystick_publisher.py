#!/usr/bin/env python
import rospy
import socket
import serial
from std_msgs.msg import String

ob1  = String()

ser = serial.Serial('/dev/ttyUSB2', 115200)

HOST = '192.168.43.21' # HOST
PORT1 = 1234
BUFFER_SIZE = 1 # Normally 1024, but I want fast response
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT1))
s.listen(1)
conn,address=s.accept()

x1 = 0
x2 = 0
x3 = 0
y1 = 0
y2 = 0
y3 = 0

count =0
def joystick_decoder(val):
    global x1,x2,x3,y1,y2,y3,count

    count+=1

    if (val & 0b11100000) == 0b00000000:
        gear = val & 0b00001111
        ha =   val & 0b00010000

    elif (val & 0b11100000) == 0b00100000:
        x1 = val & 0b00001111

    elif (val & 0b11100000) == 0b01000000:
        x2 = val & 0b00011111

    elif (val & 0b11100000) == 0b01100000:
        x3 = val & 0b00011111

    elif (val & 0b11100000) == 0b10000000:
        y1 = val & 0b00001111

    elif (val & 0b11100000) == 0b10100000:
        y2 = val & 0b00011111

    elif (val & 0b11100000) == 0b11000000:
        y3 = val & 0b00011111

    if count %7 ==0:
        x = x1
        x = (x << 5) | x2
        x = (x << 5) | x3
        y = y1
        y = (y << 5) | y2
        y = (y << 5) | y3
        count = 0
        return x,y

counter =0
def callback_joy():
    global counter
    while True:
        data_stream = conn.recv(BUFFER_SIZE)
        if ord(data_stream) == 109:
            ser.write(data_stream)
            continue

        counter+=1

        ser.write(data_stream)

        if counter % 7==0:
            x,y =joystick_decoder(ord(data_stream))
            counter = 1
            joy_values = "{} {}".format(x, y)
            print(joy_values)
            ob1.data = joy_values
            pub.publish(ob1)

        joystick_decoder(ord(data_stream))

if __name__ == '__main__':
    try:
        
        rospy.init_node('Communicator', anonymous=True,disable_signals=True)
        pub = rospy.Publisher('joystick_topic', String, queue_size=10)
        rate = rospy.Rate(50)  # 1hz
        callback_joy()

    except rospy.ROSInterruptException:
        pass

