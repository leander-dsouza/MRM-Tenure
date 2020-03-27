import pygame
import time
import subprocess
import time
import threading

print 'Rover Joystick'

mode = raw_input("Use [t]cp/ip or [s]erial: ")

pygame.init()
pygame.joystick.init()

joy = pygame.joystick.Joystick(0)
joy.init()


## SELECT MODE ##
if mode == 's':
    import serial
    ser = serial.Serial('/dev/ttyUSB0', 115200)

elif mode == 't':
    import socket
    host = '192.168.43.61'
    print host
    comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = 1234
    while True:
	try:
	    comm_sock.connect((host, port))
	    print 'opened socket at ', port
	    break
	except socket.error:
	    port += 1

    def tcp_send(data):
	    comm_sock.sendall(data)
################

check_running = True
numgears = 10
x_joy = 0
y_joy = 0
gear= 0
x_joy_last = 8000
y_joy_last = 8000
gear_last = 0
addx = 8000
addy = 8000
reconnected = False
idle = False
hill_assist = False

def check_joy():
    global check_running, x_joy, x_joy_last, y_joy, y_joy_last, reconnected, joy
    while check_running == True:
        present = False
        cmd = "lsusb | grep -o ThrustMaster"
        #cmd = "lsusb | grep -o Logitech,\ Inc.\ Extreme"

        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
        #if output == 'Logitech,\ Inc.\ Extreme\n':
        if output == 'ThrustMaster\n':
            present = True
        if present == False:
            print 'Joystick disconnected'
            reconnected = True
            y_joy = x_joy = x_joy_last = y_joy_last= 0
        if reconnected == True and present == True:
            pygame.joystick.quit()
            pygame.joystick.init()
            joy = pygame.joystick.Joystick(0)
            joy.init()
            reconnected = False

try:
    check_thread = threading.Thread(target=check_joy, args=())
    check_thread.start()

    while True:
        # time.sleep(0.01) #WHY?????? DOES THIS MAKE IT SMOOTH
        x_joy = x_joy_last
        y_joy = y_joy_last
        gear = gear_last
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    x_joy = event.value*8000 #-255 because the joystick was reverse mapped
                elif event.axis == 1:
                    y_joy = event.value*-8000
                elif event.axis == 3:
                    gear = event.value
            elif event.type == pygame.JOYBUTTONDOWN:
                if joy.get_button(1):
                    idle = not idle
		if joy.get_button(10):
		    hill_assist = not hill_assist

        if idle == True:
            print 'idle'
            x_joy = y_joy = x_joy_last = y_joy_last = 0
        x_joy_last = x_joy
        y_joy_last = y_joy
        gear_last = gear

        x_joy = int(x_joy)
        y_joy = int(y_joy)

        x_joy = x_joy + addx
        y_joy = y_joy + addy
        x_joy = max(min(16000, x_joy), 0)
        y_joy = max(min(16000, y_joy), 0)

        gear = int(((-gear+1)/2)*(numgears-1)) + 1
	print x_joy, y_joy, gear

        #print x_joy, y_joy, gear

	if hill_assist == False:
	    print "Hill assist OFF"
	    gear_pack = (0b00001111 & gear)
	elif hill_assist == True:
	    print "Hill assist ON"
	    gear_pack = (0b00001111 & gear)
	    gear_pack |= 0b00010000


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

	if mode == 's':
	    ser.write('m')
	    ser.write(chr(gear_pack))
	    ser.write(chr(x1))
	    ser.write(chr(x2))
	    ser.write(chr(x3))
	    ser.write(chr(y1))
	    ser.write(chr(y2))
	    ser.write(chr(y3))

	elif mode == 't':
	    tcp_send('m')
	    tcp_send(chr(gear_pack))
	    tcp_send(chr(x1))
	    tcp_send(chr(x2))
	    tcp_send(chr(x3))
	    tcp_send(chr(y1))
	    tcp_send(chr(y2))
	    tcp_send(chr(y3))
	    time.sleep(0.01)

except KeyboardInterrupt:
    check_running = False
    check_thread.join()
    comm_sock.close()
    pass

finally:
    check_running = False
    check_thread.join()
    comm_sock.close()
    print "Closed thread..."

print 'Exiting joystick...'
pygame.quit()
