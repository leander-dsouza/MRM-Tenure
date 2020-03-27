import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

trigPin1 = 16
echoPin1 = 18

trigPin2 = 12
echoPin2 = 22

threshold = 17

GPIO.setup(trigPin1, GPIO.OUT)
GPIO.setup(echoPin1, GPIO.IN)

GPIO.setup(trigPin2, GPIO.OUT)
GPIO.setup(echoPin2, GPIO.IN)

t1=0.000000
t2=0.000000
t3=0.000000
t4=0.000000


while 1:

    GPIO.output(trigPin1, True)
    time.sleep(0.00001)
    GPIO.output(trigPin1, False)

    while GPIO.input(echoPin1) == 0:
         pass

    t1=time.time()
    while GPIO.input(echoPin1) == 1:
        pass
    t2 = time.time()

    duration1 = t2 - t1

    distance1 = duration1*17000

    GPIO.output(trigPin2, True)
    time.sleep(0.00001)
    GPIO.output(trigPin2, False)

    while GPIO.input(echoPin2) == 0:
        pass

    t3 = time.time()
    while GPIO.input(echoPin2) == 1:
        pass

    t4 = time.time()



    duration2 = t4 - t3

    distance2 = duration2*17000


    if (distance1 > threshold) and (distance2 > threshold):
        print("FORWARD")

    elif (distance1 < threshold) and (distance2 < threshold):
        print("BACKWARD")

    elif (distance2 < threshold) and (distance2 < distance1):
        print("LEFT")

    elif (distance1 < threshold) and (distance1 < distance2):
        print("RIGHT")



GPIO.cleanup()
