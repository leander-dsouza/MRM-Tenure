const int trigPin1 = 4;
const int echoPin1 = 5;


const int trigPin2 = 2;
const int echoPin2 = 3;

//MOTOR1
const int input1=11;
const int output1=8;
//MOTOR2
const int input2=10;
const int output2=9;

long duration1,duration2;
int distance1,distance2,val1,val2;
int t1,t2,t3,t4;
int a,b;

const int threshold=17;

void setup() {
  
pinMode(trigPin1, OUTPUT); 
pinMode(echoPin1, INPUT); 


pinMode(trigPin2, OUTPUT); 
pinMode(echoPin2, INPUT); 

pinMode(input1,OUTPUT);
pinMode(output1,OUTPUT);
pinMode(input2,OUTPUT);
pinMode(output2,OUTPUT);

Serial.begin(9600); 
}


void forward()
{
  digitalWrite(input1,HIGH);
  digitalWrite(output1,HIGH);
  digitalWrite(input2,LOW);
  digitalWrite(output2,LOW);
}
void backward()
{  digitalWrite(input1,LOW);
  digitalWrite(output1,LOW);
  digitalWrite(input2,HIGH);
  digitalWrite(output2,HIGH);
}

void brutestop()
{
  digitalWrite(input1,LOW);
  digitalWrite(output1,LOW);
  digitalWrite(input2,LOW);
  digitalWrite(output2,LOW);
}
void right()
{
  digitalWrite(input1,HIGH);
  digitalWrite(output1,LOW);
  digitalWrite(input2,LOW);
  digitalWrite(output2,HIGH);
}
void left()
{
  digitalWrite(input1,LOW);
  digitalWrite(output1,HIGH);
  digitalWrite(input2,HIGH);
  digitalWrite(output2,LOW);
}




void loop() {

digitalWrite(trigPin1,HIGH);
delayMicroseconds(10);
digitalWrite(trigPin1,LOW);

while(digitalRead(echoPin1)==LOW);
t1=micros();

while(digitalRead(echoPin1)==HIGH);
t2=micros();
  
  duration1= t2-t1;
    
distance1=duration1*0.34/2;



val1= constrain(distance1,0,1000);
val1=map(val1,0,1000,0,100);

Serial.print("Value1: ");
Serial.println(val1);



//sensor2

digitalWrite(trigPin2,HIGH);
delayMicroseconds(10);
digitalWrite(trigPin2,LOW);

while(digitalRead(echoPin2)==LOW);
t3=micros();

while(digitalRead(echoPin2)==HIGH);
t4=micros();
  
  duration2= t4-t3;
      
distance2=duration2*0.34/2;



val2= constrain(distance2,0,1000);
val2=map(val2,0,1000,0,100);

Serial.print("Value2: ");
Serial.println(val2);


if((val1>threshold)&&(val2>threshold))
   {forward();
     Serial.print("FORWARD ");}

if((val1<threshold)&&(val2<threshold))
{  brutestop();
  delay(10);
  backward();
  delay(200);
   right();
   delay(500);
   Serial.print("STOP and RIGHT");}
 
if((val1<threshold)&&(val1<val2))
   { right();
     Serial.print("RIGHT ");}
     
if((val2<threshold)&&(val2<val1))
    {left();
     Serial.print("LEFT ");}
     

