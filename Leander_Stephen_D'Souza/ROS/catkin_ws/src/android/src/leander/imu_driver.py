import smbus
from math import radians

bus = smbus.SMBus(1)
g = 9.80665


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
while True:
    # TEMPERATURE
    out_temp_l = bus.read_byte_data(0x6B, 0x15)
    out_temp_h = bus.read_byte_data(0x6B, 0x16)
    out_temp = twos_complement((((out_temp_h & 0X0F) << 8) | out_temp_l), 12) / 16 + 25
    print("temp:", out_temp, "degrees C")
    print("")

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
    #print("gyro",out_x_g, out_y_g, out_z_g, "rad/s")
    #print("") # \r\n"

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
    #print("acc:", out_x_xl, out_y_xl, out_z_xl, "m/s2")
    #print("")  # \r\n

    # MAGNETOMETER
    out_x_m_l = bus.read_byte_data(0x1E, 0x28)
    out_x_m_h = bus.read_byte_data(0x1E, 0x29)
    out_x_m = twos_complement((out_x_m_h << 8) | out_x_m_l, 16)
    out_x_m = (arduino_map(out_x_m, -32768, 32767, -4, 4)) / 1e4       #1 gauss = 1e-4 tesla

    out_y_m_l = bus.read_byte_data(0x1E, 0x2A)
    out_y_m_h = bus.read_byte_data(0x1E, 0x2B)
    out_y_m = twos_complement((out_y_m_h << 8) | out_y_m_l, 16)
    out_y_m = (arduino_map(out_y_m, -32768, 32767, -4, 4)) / 1e4

    out_z_m_l = bus.read_byte_data(0x1E, 0x2C)
    out_z_m_h = bus.read_byte_data(0x1E, 0x2D)
    out_z_m = twos_complement((out_z_m_h << 8) | out_z_m_l, 16)
    out_z_m = (arduino_map(out_z_m, -32768, 32767, -4, 4)) / 1e4
    #print("mag:", out_x_m,out_y_m,out_z_m, "tesla")
    #print("") # \r\n
