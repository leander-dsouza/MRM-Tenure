import smbus
import time
import math


min_x=0
max_x=0
min_y=0
max_y=0
min_z=0
max_z=0

bus = smbus.SMBus(1)

def twos_complement(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return float(val)


def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
bus.write_byte_data(0x1E, 0x20, 0b01111100)
bus.write_byte_data(0x1E, 0x21, 0b00000000)
bus.write_byte_data(0x1E, 0x22, 0b00000000)
bus.write_byte_data(0x1E, 0x23, 0b00001100)


while(True):

    out_x_m_l = bus.read_byte_data(0x1E, 0x28)
    out_x_m_h = bus.read_byte_data(0x1E, 0x29)
    x = twos_complement((out_x_m_h << 8) | out_x_m_l, 16)
    x = (arduino_map(x, -32768, 32767, -4, 4)) / 1e4    # 1 gauss = 1e-4 tesla
    #print("X=", x, "tesla")



    out_y_m_l = bus.read_byte_data(0x1E, 0x2A)
    out_y_m_h = bus.read_byte_data(0x1E, 0x2B)
    y= twos_complement((out_y_m_h << 8) | out_y_m_l, 16) 
    y = (arduino_map(y, -32768, 32767, -4, 4)) / 1e4
    #print("Y=", y, "tesla")


    out_z_m_l = bus.read_byte_data(0x1E, 0x2C)
    out_z_m_h = bus.read_byte_data(0x1E, 0x2D)
    z = twos_complement((out_z_m_h << 8) | out_z_m_l, 16) 
    z = (arduino_map(z, -32768, 32767, -4, 4)) / 1e4
    #print("Z=",z, "tesla")

    print("")

    if x< min_x:
        min_x=x
    if x>max_x:
        max_x=x

    if y< min_y:
        min_y=y
    if y>max_y:
        max_y=y

    if z< min_z:
        min_z=z
    if z>max_z:
        max_z=z

    offset_x= (max_x + min_x) / 2
    offset_y =(max_y + min_y) / 2
    offset_z =(max_z + min_z) / 2

    x_soft = x-offset_x
    y_soft = y-offset_y
    z_soft = z-offset_z


    degree= math.atan2(y_soft,x_soft)*180/math.pi

    if degree<0:
        degree +=360



    print("HEADING:", degree)
