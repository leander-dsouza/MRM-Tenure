import rospy
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion
import math as m
import time
import numpy
from pyproj import Geod
import geopy
from geopy.distance import VincentyDistance
import serial
from std_msgs.msg import String

#INITIALIZATION BLOCK
wgs84_geod = Geod(ellps='WGS84')

#given_lat and given_lon are given GPS in gazebo (4th box left of the rover at the end of platform)
given_lat = 13.347686666666668
given_lon = 74.792111666666667

apun_ka_gps_error = 2
count = 0
flag = 0
gear = 2

array_of_waypoints = []
curr_lat = 0 
curr_lon = 0

def bearing(lon1, lat1, lon2, lat2):
	global bearing_angle
	dLon = lon2 - lon1
	y = m.sin(dLon) * m.cos(lat2)
	x = m.cos(lat1) * m.sin(lat2) - m.sin(lat1) * m.cos(lat2) * m.cos(dLon)

	bearing_angle = m.atan2(y, x) * 180 / m.pi

	if bearing_angle < 0:
		bearing_angle += 360

	return bearing_angle

def go_straight(way_lat,way_lon):
	global iteration,heading
	bear,rev_bear,dist = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
	b = bearing(curr_lon, curr_lat, way_lon, way_lat)
	if bear<0:
		bear+=360
	new_dist = 100
	prev_time = time.time()
	while dist>1:
		forward()
		bear,rev_bear,dist = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
		if bear<0:
			bear+=360
		print('head',heading,'bear',bear,'dist',dist)
		new_time = time.time()
		if abs(heading-bear)>10:
			correct_heading(way_lat, way_lon)
		if new_time-prev_time>4:
			_,_,new_dist = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
			prev_time = time.time()
		if new_dist<dist:
			print('broken','dist',dist,'new_dist',new_dist)
			break
	brutestop()

def correct_heading(way_lat,way_lon):
	global curr_lat,curr_lon, heading, dist, flag,b, iteration
	bear,rev_bear,dist = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
	b = bearing(curr_lon, curr_lat, way_lon, way_lat)
	if bear<0:
		bear+=360
	if flag == 0:
		while(heading-bear>0 and heading-bear<180):
			bear,rev_bear,_ = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
			#print('1','h',heading,'b',bear,'i',iteration,'rot')
			if bear<0:
				bear+=360
			print('head',heading,'bear',bear)
			left()
			flag = 1
			if abs(heading-bear)<10:
				break
		while(heading-bear<-180):
			bear,rev_bear,_ = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
			#print('2','h',heading,'b',bear,'i',iteration,'rot')
			if bear<0:
				bear+=360
			print('head',heading,'bear',bear)
			left()
			flag = 1 
			if abs(heading-bear)<10:
				break

		if flag == 1:	
			brutestop()	
			go_straight(way_lat,way_lon)

	if flag == 0:
		while(heading-bear>=180):
			bear,rev_bear,_ = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
			#print('3','h',heading,'b',bear,'i',iteration,'rot')
			if bear<0:
				bear+=360
			print('head',heading,'bear',bear)
			right()
			flag = 1
			if abs(heading-bear)<10:
				break
		while(heading-bear<0 and heading-bear>=-180):
			bear,rev_bear,_ = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
			#print('4','h',heading,'b',bear,'i',iteration,'rot')
			if bear<0:
				bear+=360
			print('head',heading,'bear',bear)
			right()
			flag = 1
			if abs(heading-bear)<10:
				break

		if flag == 1:	
			brutestop()	
			go_straight(way_lat,way_lon)

	if flag == 0:
		while(heading-bear>=180):
			bear,rev_bear,_ = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
			#print('5','h',heading,'b',bear,'i',iteration,'rot')
			if bear<0:
				bear+=360
			print('head',heading,'bear',bear)
			right()
			flag = 1
			if abs(heading-bear)<10:
				break
		while(heading-bear<0 and heading-bear>=-180):
			bear,rev_bear,_ = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
			#print('6','h',heading,'b',bear,'i',iteration,'rot')
			if bear<0:
				bear+=360
			print('head',heading,'bear',bear)
			right()
			flag = 1
			if abs(heading-bear)<10:
				break

		if flag == 1:	
			brutestop()	
			go_straight(way_lat,way_lon)

	if flag == 0:
		while(heading-bear>0 and heading-bear<180):
			bear,rev_bear,_ = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
			#print('7','h',heading,'b',bear,'i',iteration,'rot')
			if bear<0:
				bear+=360
			print('head',heading,'bear',bear)
			left()
			flag = 1
			if abs(heading-bear)<10:
				break
		while(heading-bear<-180):
			bear,rev_bear,_ = wgs84_geod.inv(curr_lon, curr_lat, way_lon, way_lat)
			#print('8','h',heading,'b',bear,'i',iteration,'rot')
			if bear<0:
				bear+=360
			print('head',heading,'bear',bear)
			left()
			flag = 1 
			if abs(heading-bear)<10:
				break

		if flag == 1:	
			brutestop()	
			go_straight(way_lat,way_lon)




def generate_4_coordinates():
	global center_lat, center_lon, iteration, flag
	origin = geopy.Point(center_lat,center_lon)

	destination1 = VincentyDistance(meters= 4.94974746831).destination(origin, 315)
	lat1,lon1 = destination1.latitude, destination1.longitude
	
	destination2 = VincentyDistance(meters= 4.94974746831).destination(origin, 45)
	lat2,lon2 = destination2.latitude, destination2.longitude
	
	destination3 = VincentyDistance(meters= 4.94974746831).destination(origin, 135)
	lat3,lon3 = destination3.latitude, destination3.longitude

	destination4 = VincentyDistance(meters= 4.94974746831).destination(origin, 225)
	lat4,lon4 = destination4.latitude, destination4.longitude

	origin_c1 = geopy.Point(lat1,lon1)
	origin_c2 = geopy.Point(lat2,lon2)
	origin_c3 = geopy.Point(lat3,lon3)
	origin_c4 = geopy.Point(lat4,lon4)
	

	hex_coordinates_c1(origin_c1)
	hex_coordinates_c2(origin_c2)
	hex_coordinates_c3(origin_c3)
	hex_coordinates_c4(origin_c4)


	for iteration in range(0, 18):
		#rotate_360()
		correct_heading(array_of_waypoints[iteration][0],array_of_waypoints[iteration][1])
		flag = 0


def rotate_360():
	global heading
	now_heading = heading
	prev_time = time.time()
	while True:
		right()
		now_time = time.time()
		if (now_time-prev_time)>3:
			break
	while True:
		if abs(now_heading-heading)<2:
			brutestop()
			break



def update_line(hl, new_data_lat, new_data_lon):
	hl.set_xdata(numpy.append(hl.get_xdata(), new_data_lat))
	hl.set_ydata(numpy.append(hl.get_ydata(), new_data_lon))


def hex_coordinates_c1(org):
	global array_of_waypoints
	dest_c1_1 = VincentyDistance(meters=3.5).destination(org, 180)
	lat_c1_1, lon_c1_1 = dest_c1_1.latitude, dest_c1_1.longitude
	array_of_waypoints.append([lat_c1_1,lon_c1_1])
	dest_c1_2 = VincentyDistance(meters=3.5).destination(org, 240)
	lat_c1_2, lon_c1_2 = dest_c1_2.latitude, dest_c1_2.longitude
	array_of_waypoints.append([lat_c1_2,lon_c1_2])
	dest_c1_3 = VincentyDistance(meters=3.5).destination(org, 300)
	lat_c1_3, lon_c1_3 = dest_c1_3.latitude, dest_c1_3.longitude
	array_of_waypoints.append([lat_c1_3,lon_c1_3])
	dest_c1_4 = VincentyDistance(meters=3.5).destination(org, 0)
	lat_c1_4, lon_c1_4 = dest_c1_4.latitude, dest_c1_4.longitude
	array_of_waypoints.append([lat_c1_4,lon_c1_4])
	dest_c1_5 = VincentyDistance(meters=3.5).destination(org, 60)
	lat_c1_5, lon_c1_5 = dest_c1_5.latitude, dest_c1_5.longitude
	array_of_waypoints.append([lat_c1_5,lon_c1_5])


def hex_coordinates_c2(org):
	global array_of_waypoints
	dest_c2_1 = VincentyDistance(meters=3.5).destination(org, 240)
	lat_c2_1, lon_c2_1 = dest_c2_1.latitude, dest_c2_1.longitude
	array_of_waypoints.append([lat_c2_1,lon_c2_1])
	dest_c2_2 = VincentyDistance(meters=3.5).destination(org, 180)
	lat_c2_2, lon_c2_2 = dest_c2_2.latitude, dest_c2_2.longitude
	array_of_waypoints.append([lat_c2_2,lon_c2_2])
	dest_c2_3 = VincentyDistance(meters=3.5).destination(org, 120)
	lat_c2_3, lon_c2_3 = dest_c2_3.latitude, dest_c2_3.longitude
	array_of_waypoints.append([lat_c2_3,lon_c2_3])
	dest_c2_4 = VincentyDistance(meters=3.5).destination(org, 60)
	lat_c2_4, lon_c2_4 = dest_c2_4.latitude, dest_c2_4.longitude
	array_of_waypoints.append([lat_c2_4,lon_c2_4])
	dest_c2_5 = VincentyDistance(meters=3.5).destination(org, 0)
	lat_c2_5, lon_c2_5 = dest_c2_5.latitude, dest_c2_5.longitude
	array_of_waypoints.append([lat_c2_5,lon_c2_5])


def hex_coordinates_c3(org):
	global array_of_waypoints
	dest_c3_1 = VincentyDistance(meters=3.5).destination(org, 300)
	lat_c3_1, lon_c3_1 = dest_c3_1.latitude, dest_c3_1.longitude
	array_of_waypoints.append([lat_c3_1,lon_c3_1])
	dest_c3_2 = VincentyDistance(meters=3.5).destination(org, 240)
	lat_c3_2, lon_c3_2 = dest_c3_2.latitude, dest_c3_2.longitude
	array_of_waypoints.append([lat_c3_2,lon_c3_2])
	dest_c3_3 = VincentyDistance(meters=3.5).destination(org, 180)
	lat_c3_3, lon_c3_3 = dest_c3_3.latitude, dest_c3_3.longitude
	array_of_waypoints.append([lat_c3_3,lon_c3_3])
	dest_c3_4 = VincentyDistance(meters=3.5).destination(org, 120)
	lat_c3_4, lon_c3_4 = dest_c3_4.latitude, dest_c3_4.longitude
	array_of_waypoints.append([lat_c3_4,lon_c3_4])
	dest_c3_5 = VincentyDistance(meters=3.5).destination(org, 60)
	lat_c3_5, lon_c3_5 = dest_c3_5.latitude, dest_c3_5.longitude
	array_of_waypoints.append([lat_c3_5,lon_c3_5])


def hex_coordinates_c4(org):
	global array_of_waypoints
	dest_c4_1 = VincentyDistance(meters=3.5).destination(org, 300)
	lat_c4_1, lon_c4_1 = dest_c4_1.latitude, dest_c4_1.longitude
	array_of_waypoints.append([lat_c4_1,lon_c4_1])
	dest_c4_2 = VincentyDistance(meters=3.5).destination(org, 240)
	lat_c4_2, lon_c4_2 = dest_c4_2.latitude, dest_c4_2.longitude
	array_of_waypoints.append([lat_c4_2,lon_c4_2])
	dest_c4_3 = VincentyDistance(meters=3.5).destination(org, 180)
	lat_c4_3, lon_c4_3 = dest_c4_3.latitude, dest_c4_3.longitude
	array_of_waypoints.append([lat_c4_3,lon_c4_3])


ser = serial.Serial(
	port='/dev/ttyUSB1',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

def joystick_encoder(x_joy,y_joy,gear):
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

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

aligner = 0
heading = 0

def callback_imu(msg):
	global heading, curr_lon, curr_lat, given_lon, given_lat

	orientation_list = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
	(roll, pitch, yaw) = euler_from_quaternion(orientation_list)
#(-3.12-3.12) -- for quaternion(not gazebo)

	if yaw>=0:
		heading = map(yaw, 0, 3.12, 0, 180)
		heading = (heading + aligner) % 360

	else:
		heading = map(yaw, -3.12, 0, 180, 360)
		heading = (heading + aligner) % 360



def callback_gps(msg):
	global curr_lat, curr_lon
	curr_lat = msg.latitude
	curr_lon = msg.longitude
	#print(curr_lat,curr_lon)
########This function gives bearing and distance between 2 gps points
def bear_N_dist(start_lon, start_lat, next_lon, next_lat):
	global heading
	(bearing, rev_bearing, dist) = wgs84_geod.inv(start_lon, start_lat, next_lon, next_lat)
	print('head',heading,'bear',bearing,'dist',dist)
	if dist>800:
		return
	if bearing<0:
		bearing = bearing+360
	return bearing,dist


def talk_listen():
	global curr_lat, curr_lon, center_lat, center_lon, count, apun_ka_gps_error

	rospy.Subscriber("/imu_perfected", Imu, callback_imu)
	rospy.Subscriber("/fix", NavSatFix, callback_gps)
	#rospy.Subscriber("/gps/filtered", NavSatFix, callback_gps)

	while not rospy.is_shutdown():
		
		bearing_angle,dist_from_initial=bear_N_dist(curr_lon, curr_lat, given_lon, given_lat)
		print('distance from initial point',dist_from_initial)
		if dist_from_initial<apun_ka_gps_error and count == 0:
			print("BALL SEARCH ACTIVATED")
			count = 1
			center_lat = curr_lat
			center_lon = curr_lon
			generate_4_coordinates()
		rate.sleep()



if __name__ == '__main__':
	try:
		
		rospy.init_node('talker',anonymous=True,disable_signals=True)
		rate = rospy.Rate(50)
		talk_listen()
	except rospy.ROSInterruptException:
		pass
