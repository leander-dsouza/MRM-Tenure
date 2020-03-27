#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu, MagneticField,Temperature
import smbus
from math import radians

bus = smbus.SMBus(1)
g = 9.80665

ob1 = Imu()
ob2 = MagneticField()
ob3 = Temperature()

ob1.header.frame_id = 'imu'
ob1.orientation_covariance = [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

ob2.header.frame_id = 'mag'
ob3.header.frame_id = 'temp'


def twos_complement(val, bits):
    if (val & (1 << (bits - 1))) != 0:  # if first bit is one (negative)
        val = val - (1 << bits)
    return float(val)


def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# enable gyroscope-
bus.write_byte_data(0x6B, 0x10, 0b11000011)  # +-245 deg/s

# enable accelerometer
bus.write_byte_data(0x6B, 0x1F, 0b01111000)
bus.write_byte_data(0x6B, 0x20, 0b11000000)  # +-2g
bus.write_byte_data(0x6B, 0x21, 0b11000000)

# enable magnetometer
bus.write_byte_data(0x1E, 0x20, 0b11111100)
bus.write_byte_data(0x1E, 0x21, 0b00000000)  # +-4 gauss
bus.write_byte_data(0x1E, 0x22, 0b00000000)
bus.write_byte_data(0x1E, 0x23, 0b00001100)

# The output scale for any setting is [-32768, +32767] (-2^8 -> 2^7-1) for each of the six axes
def callback_imu():
    while True:
        time = rospy.Time.now()
        # TEMPERATURE
        out_temp_l = bus.read_byte_data(0x6B, 0x15)
        out_temp_h = bus.read_byte_data(0x6B, 0x16)
        out_temp = twos_complement((((out_temp_h & 0X0F) << 8) | out_temp_l), 12) / 16 + 25
        ob3.temperature = out_temp
        pub_t.publish(ob3)

        # GYROSCOPE
        out_x_g_l = bus.read_byte_data(0x6B, 0x18)
        out_x_g_h = bus.read_byte_data(0x6B, 0x19)
        out_x_g = twos_complement((out_x_g_h << 8) | out_x_g_l, 16)
        out_x_g = arduino_map(out_x_g, -32768, 32767, -245, 245)
        out_x_g = radians(out_x_g)

        out_y_g_l = bus.read_byte_data(0x6B, 0x1A)
        out_y_g_h = bus.read_byte_data(0x6B, 0x1B)
        out_y_g = twos_complement((out_y_g_h << 8) | out_y_g_l, 16)
        out_y_g = arduino_map(out_y_g, -32768, 32767, -245, 245)
        out_y_g = radians(out_y_g)

        out_z_g_l = bus.read_byte_data(0x6B, 0x1C)
        out_z_g_h = bus.read_byte_data(0x6B, 0x1D)
        out_z_g = twos_complement((out_z_g_h << 8) | out_z_g_l, 16)
        out_z_g = arduino_map(out_z_g, -32768, 32767, -245, 245)
        out_z_g = radians(out_z_g)


        # ACCELEROMETER
        out_x_xl_l = bus.read_byte_data(0x6B, 0x28)
        out_x_xl_h = bus.read_byte_data(0x6B, 0x29)
        out_x_xl = twos_complement((out_x_xl_h << 8) | out_x_xl_l, 16)
        out_x_xl = arduino_map(out_x_xl, -32768, 32767, -2 * g, 2 * g)

        out_y_xl_l = bus.read_byte_data(0x6B, 0x2A)
        out_y_xl_h = bus.read_byte_data(0x6B, 0x2B)
        out_y_xl = twos_complement((out_y_xl_h << 8) | out_y_xl_l, 16)
        out_y_xl = arduino_map(out_y_xl, -32768, 32767, -2 * g, 2 * g)

        out_z_xl_l = bus.read_byte_data(0x6B, 0x2C)
        out_z_xl_h = bus.read_byte_data(0x6B, 0x2D)
        out_z_xl = twos_complement((out_z_xl_h << 8) | out_z_xl_l, 16)
        out_z_xl = arduino_map(out_z_xl, -32768, 32767, -2 * g, 2 * g)

        ob1.header.stamp = time
        ob1.angular_velocity.x = out_x_g
        ob1.angular_velocity.y = out_y_g
        ob1.angular_velocity.z = out_z_g
        ob1.linear_acceleration.x = out_x_xl
        ob1.linear_acceleration.y = out_y_xl
        ob1.linear_acceleration.z = out_z_xl
        pub_i.publish(ob1)


        # MAGNETOMETER
        out_x_m_l = bus.read_byte_data(0x1E, 0x28)
        out_x_m_h = bus.read_byte_data(0x1E, 0x29)
        out_x_m = twos_complement((out_x_m_h << 8) | out_x_m_l, 16)
        out_x_m = (arduino_map(out_x_m, -32768, 32767, -4, 4)) / 1e4  # 1 gauss = 1e-4 tesla

        out_y_m_l = bus.read_byte_data(0x1E, 0x2A)
        out_y_m_h = bus.read_byte_data(0x1E, 0x2B)
        out_y_m = twos_complement((out_y_m_h << 8) | out_y_m_l, 16)
        out_y_m = (arduino_map(out_y_m, -32768, 32767, -4, 4)) / 1e4

        out_z_m_l = bus.read_byte_data(0x1E, 0x2C)
        out_z_m_h = bus.read_byte_data(0x1E, 0x2D)
        out_z_m = twos_complement((out_z_m_h << 8) | out_z_m_l, 16)
        out_z_m = (arduino_map(out_z_m, -32768, 32767, -4, 4)) / 1e4

        ob2.header.stamp = time
        ob2.magnetic_field.x = out_x_m
        ob2.magnetic_field.y = out_y_m
        ob2.magnetic_field.z = out_z_m
        pub_m.publish(ob2)


if __name__ == '__main__':
    try:
        rospy.init_node('imu_publisher', anonymous=True)
        pub_i = rospy.Publisher('imu_data/raw', Imu, queue_size=10)
        pub_m = rospy.Publisher('mag_data/raw', MagneticField, queue_size=10)
        pub_t = rospy.Publisher('temp_data/raw',Temperature, queue_size=10)
        rate = rospy.Rate(50)  # 50hz
        callback_imu()

    except rospy.ROSInterruptException:
        pass

