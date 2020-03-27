import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#frequency=100Hz

ledpin=35

t_on=0.00
t_off=0.00
GPIO.setup(ledpin,GPIO.OUT)

def pwm(pin,a):
    d_cycle=a*1.000000/255.000000
    t_on = d_cycle*0.01
    t_off =0.01-t_on
      
    t1=time.time()
    
    while(True):  
        
         
        t2=time.time()
        t3=t2-t1
        if(t3<t_on):
	 	GPIO.output(ledpin, True)
        else:
		break

    t4=time.time()

    while(True):
	t5=time.time()
        t6=t5-t4
	if(t6<t_off):
		GPIO.output(ledpin, False)
        else:
		break


while(True):

                for x in range (0,255,1)     
   			pwm(ledpin,x)
      
GPIO.cleanup()     
