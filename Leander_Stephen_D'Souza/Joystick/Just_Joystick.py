import pygame
from pygame import locals

def arduino_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


pygame.init()

pygame.joystick.init() # main joystick device system

try:
	j = pygame.joystick.Joystick(0) # create a joystick instance
	j.init() # init instance
	print ("Enabled joystick:")
except pygame.error:
	print ("no joystick found.")

while 1:
	for e in pygame.event.get(): # iterate over event stack
                if e.type == pygame.locals.JOYAXISMOTION:
                    x ,y =  j.get_axis(0) ,j.get_axis(1)
                    x= np.round(arduino_map(x, -1, 1, 0, 1024))
                    y= np.round(arduino_map(y, 1, -1, 0, 1024))
                    print("X=",x)
                    print("Y=",y)
