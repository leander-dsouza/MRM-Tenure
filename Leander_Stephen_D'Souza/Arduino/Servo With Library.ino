
#include<Servo.h>
 Servo champ; // creates 12 objects of servo
 int i=0;




void setup() {
  // put your setup code here, to run once:

champ.attach(10);//PWM through pin 10
}

void loop() {
  // put your main code here, to run repeatedly:

for (i=0; i<=180;i++)
{
     champ.write(i);// servo goes to pos
     delay(10);}
     
for (i=180; i>=0;i--)
{
     champ.write(i);// servo goes to pos
     delay(10);}
     
}
