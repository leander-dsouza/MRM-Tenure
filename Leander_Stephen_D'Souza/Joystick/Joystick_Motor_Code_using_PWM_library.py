import RPi.GPIO as GPIO
import time
import pygame
from pygame import locals
import pygame.display

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

speedA = 0.000
speedB = 0.000

x = 512.00
y = 512.00

# frequency=100Hz

t_on = 0.00
t_off = 0.00

ledpin1 =35  # left_fwd
ledpin2 =36  # right_fwd
ledpin3 =37  # left_bck
ledpin4 =38  # right_bck

GPIO.setup(ledpin1, GPIO.OUT)
GPIO.setup(ledpin2, GPIO.OUT)
GPIO.setup(ledpin3, GPIO.OUT)
GPIO.setup(ledpin4, GPIO.OUT)

GPIO.output(ledpin1, False)
GPIO.output(ledpin2, False)
GPIO.output(ledpin3, False)
GPIO.output(ledpin4, False)

p=GPIO.PWM(ledpin1,100)
q=GPIO.PWM(ledpin2,100)
r=GPIO.PWM(ledpin3,100)
s=GPIO.PWM(ledpin4,100)

p.start(0.00)
q.start(0.00)
r.start(0.00)
s.start(0.00)

def arduino_map(x, in_min, in_max, out_min, out_max):
    return ((x - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min


def oct1(x, y):
    speedA = arduino_map(y, 1023, 512, 255, 0)
    speedB = arduino_map(x + y, 1535, 1023, 255, 0)
    p.ChangeDutyCycle(speedA*(100.000000/255.000000))
    q.ChangeDutyCycle(speedB*(100.000000/255.000000))
    r.ChangeDutyCycle(0)	
    s.ChangeDutyCycle(0)

def oct2(x, y):
    speedA = arduino_map(x, 512, 0, 0, 255)
    speedB = arduino_map(x + y, 1023, 512, 0, 255)
    p.ChangeDutyCycle(speedA*(100.000000/255.000000))
    s.ChangeDutyCycle(speedB*(100.000000/255.000000))
    q.ChangeDutyCycle(0)	
    r.ChangeDutyCycle(0)


def oct3(x, y):
    speedA = arduino_map(y - x, 512, 0, 255, 0)
    speedB = arduino_map(x, 512, 0, 0, 255)
    p.ChangeDutyCycle(speedA*(100.000000/255.000000))
    s.ChangeDutyCycle(speedB*(100.000000/255.000000))
    r.ChangeDutyCycle(0)	
    q.ChangeDutyCycle(0)

def oct4(x, y):
    speedA = arduino_map(x - y, 512, 0, 255, 0)
    speedB = arduino_map(y, 512, 0, 0, 255)
    r.ChangeDutyCycle(speedA*(100.000000/255.000000))
    s.ChangeDutyCycle(speedB*(100.000000/255.000000))
    p.ChangeDutyCycle(0)	
    q.ChangeDutyCycle(0)

def oct5(x, y):
    speedA = arduino_map(y, 512, 0, 0, 255)
    speedB = arduino_map(x + y, 1023, 512, 0, 255)
    r.ChangeDutyCycle(speedA*(100.000000/255.000000))
    s.ChangeDutyCycle(speedB*(100.000000/255.000000))
    p.ChangeDutyCycle(0)	
    q.ChangeDutyCycle(0)


def oct6(x, y):
    speedA = arduino_map(x, 1023, 512, 255, 0)
    speedB = arduino_map(x + y, 1535, 1023, 255, 0)
    r.ChangeDutyCycle(speedA*(100.000000/255.000000))
    q.ChangeDutyCycle(speedB*(100.000000/255.000000))
    p.ChangeDutyCycle(0)	
    s.ChangeDutyCycle(0)


def oct7(x, y):
    speedA = arduino_map(x - y, 0, 512, 0, 255)
    speedB = arduino_map(x, 1023, 512, 255, 0)
    r.ChangeDutyCycle(speedA*(100.000000/255.000000))
    q.ChangeDutyCycle(speedB*(100.000000/255.000000))
    p.ChangeDutyCycle(0)	
    s.ChangeDutyCycle(0)


def oct8(x, y):
    speedA = arduino_map(y - x, 0, 512, 0, 255)
    speedB = arduino_map(y, 1023, 512, 255, 0)
    p.ChangeDutyCycle(speedA*(100.000000/255.000000))
    q.ChangeDutyCycle(speedB*(100.000000/255.000000))
    r.ChangeDutyCycle(0)	
    s.ChangeDutyCycle(0)


pygame.init()
pygame.display.init()
pygame.joystick.init()  # main joystick device system

try:
    j = pygame.joystick.Joystick(0)  # create a joystick instance
    j.init()  # init instance
    print("Enabled joystick:")
except pygame.error:
    print("no joystick found.")

while 1:
    for e in pygame.event.get():  # iterate over event stack
        if e.type == pygame.locals.JOYAXISMOTION:
            x, y = j.get_axis(0), j.get_axis(1)
            x = round(arduino_map(x, -1, 1, 1023, 0))
            y = round(arduino_map(y, 1, -1, 0, 1023))
            print("X=", x)
            print("Y=", y)

            # QUAD 1
            if (x <= 512) & ((y >= 512) & (y <= 1023)):

                if (x + y) >= 1023:  # OCT1
                    oct1(x, y)

                if (x + y) < 1023:  # OCT2
                    oct2(x, y)

            # QUAD 2
            if (x <= 512) & (y <= 512):

                if (x - y) <= 0:  # OCT3
                    oct3(x, y)

                if (x - y) > 0:  # OCT4
                    oct4(x, y)

            # QUAD 3
            if ((x >= 512) & (x <= 1023)) & (y <= 512):

                if (x + y) <= 1023:  # OCT5
                    oct5(x, y)

                if (x + y) > 1023:  # OCT6
                    oct6(x, y)

            # QUAD 4
            if ((x >= 512) & (x <= 1023)) & ((y >= 512) & (y <= 1023)):

                if (y - x) <= 0:  # OCT7
                    oct7(x, y)

                if (y - x) > 0:  # OCT8
                    oct8(x, y)
