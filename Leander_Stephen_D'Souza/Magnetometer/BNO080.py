import time
import BNO080 as B
mag = B.BNO080(B.BNO080_ADDRESS_B)
mag.begin()
mag.enable_magnetometer(50)

def goto(linenum):
    global line
    line = linenum


t1=time.sleep()
while True:

    if mag.data_available is True:
        t2=time.sleep()
        if t2-t1<30.000:
            x,y,z = mag.get_mag()
            print('x:',x,'y:',y,'z:',z)
        else:
            goto(12)
