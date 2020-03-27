import serial
import base64

image = open(r'/home/pi/tennis.jpg', 'rb')
image_read = image.read()
image_64_encode = base64.encodestring(image_read)
print(image_64_encode)

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser.write(image_64_encode)
print(len(image_64_encode))
