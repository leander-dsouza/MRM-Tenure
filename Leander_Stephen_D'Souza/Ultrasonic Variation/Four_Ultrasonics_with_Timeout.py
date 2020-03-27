import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# left forward

trigPin1 = 27
echoPin1 = 17

# right forward

trigPin2 = 14
echoPin2 = 15

# left back

trigPin3 = 26
echoPin3 = 19

# right back

trigPin4 = 20
echoPin4 = 21

threshold = 17

GPIO.setup(trigPin1, GPIO.OUT)
GPIO.setup(echoPin1, GPIO.IN)

GPIO.setup(trigPin2, GPIO.OUT)
GPIO.setup(echoPin2, GPIO.IN)

GPIO.setup(trigPin3, GPIO.OUT)
GPIO.setup(echoPin3, GPIO.IN)

GPIO.setup(trigPin4, GPIO.OUT)
GPIO.setup(echoPin4, GPIO.IN)

t1 = 0.000000
t2 = 0.000000
t3 = 0.000000
t4 = 0.000000
t5 = 0.000000
t6 = 0.000000

tax1 = 0.000000
tax2 = 0.000000
tax3 = 0.000000
tax4 = 0.000000


def ultrasonic():
    while 1:

        time.sleep(0.1)
        GPIO.output(trigPin1, True)
        time.sleep(0.00001)
        GPIO.output(trigPin1, False)

        while GPIO.input(echoPin1) == 0:
            pass

        t1 = time.time()

        while GPIO.input(echoPin1) == 1:
            t2 = time.time()
            tax1 = t2 - t1
            i = 0
            if tax1 > 0.005:
                i = 1
                break

        t2 = time.time()

        duration1 = t2 - t1

        distance1 = duration1 * 17000
        # .............................................
        GPIO.output(trigPin2, True)
        time.sleep(0.00001)
        GPIO.output(trigPin2, False)

        while GPIO.input(echoPin2) == 0:
            pass

        t3 = time.time()

        while GPIO.input(echoPin2) == 1:
            t4 = time.time()
            tax2 = t4 - t3
            j = 0
            if tax2 > 0.005:
                j = 2
                break

        t4 = time.time()

        if (i + j) == 3:
            print("FORWARD")

        duration2 = t4 - t3

        distance2 = duration2 * 17000

        if (distance1 > threshold) and (distance2 > threshold):
            print("FORWARD")

        elif (distance1 < threshold) and (distance2 < threshold):
            print("BACKWARD")
            return -1

        elif (distance2 < threshold) and (distance2 < distance1):
            print("LEFT")
            return -1

        elif (distance1 < threshold) and (distance1 < distance2):
            print("RIGHT")
            return -1

        # SIDE ULTRASONICS..........................................................................................

        GPIO.output(trigPin3, True)
        time.sleep(0.00001)
        GPIO.output(trigPin3, False)

        while GPIO.input(echoPin3) == 0:
            pass

        t5 = time.time()

        while GPIO.input(echoPin3) == 1:
            t6 = time.time()
            tax3 = t6 - t5
            get = 0
            if tax3 > 0.005:
                get = 1
                break

        t6 = time.time()

        if get == 1:
            print("FORWARD--")
            return 1

        duration3 = t6 - t5

        distance3 = duration3 * 17000

        if distance3 < threshold:
            print("FORWARD---")
            return 1
        ##......................................................................................................

        GPIO.output(trigPin4, True)
        time.sleep(0.00001)
        GPIO.output(trigPin4, False)

        while GPIO.input(echoPin4) == 0:
            pass

        t7 = time.time()

        while GPIO.input(echoPin4) == 1:
            t8 = time.time()
            tax4 = t8 - t7
            put = 0
            if tax4 > 0.005:
                put = 2
                break

        t8 = time.time()

        if put == 2:
            print("FORWARD--")
            return 1

        duration4 = t8 - t7

        distance4 = duration4 * 17000

        if distance4 < threshold:
            print("FORWARD---")
            return 1

        # ..............................................................................................................

        GPIO.cleanup()

while 1:

   ultrasonic()
