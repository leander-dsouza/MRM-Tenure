
int angle;
float pwm;
const int servopin=7;



void setup() {
  // put your setup code here, to run once:
pinMode(servopin,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

for(angle=0;angle<=180;angle+=5)
servopulse(angle);

for(angle=180;angle>=0;angle-=5)
servopulse(angle);

}

void servopulse(int angle)
{int servo;
   pwm=map(angle,0,180,1000,2900);
     
   digitalWrite(servopin,HIGH);
   delayMicroseconds(pwm);
   digitalWrite(servopin,LOW);
   delay(50);
}
