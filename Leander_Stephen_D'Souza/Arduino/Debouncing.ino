
const int trigPin=7;
const int echoPin=3;
const int ledpin1=8;
const int ledpin2=9;
const int ledpin3=10;
long int t;
long int distance;
long int value;

const int button1 = 12;

boolean lastButton = LOW;
boolean currentButton = LOW;


void setup()
{
  pinMode(switchPin, INPUT);
  pinMode(echoPin,INPUT);
  pinMode(trigPin,OUTPUT);
  pinMode(ledpin1,OUTPUT);
  pinMode(ledpin2,OUTPUT);
  pinMode(ledpin3,OUTPUT);
  
  
  Serial.begin(9600);
}

boolean debounce(boolean last)
{
  boolean current = digitalRead(button1);
  if (last != current)
  {
    delay(5);
    current = digitalRead(button1);
  }
  return current;
}

void loop()
{
  currentButton = debounce(lastButton);
  if (lastButton == LOW && currentButton == HIGH)
  {
     digitalWrite(trigPin, LOW);
  delay(10);

  
  digitalWrite(trigPin,HIGH);
  delay(50);
  digitalWrite(trigPin,LOW);
  
t =pulseIn(echoPin, HIGH);

distance= (t*0.034/2);
Serial.print("Value: ");

constrain(distance,0,100);

value=map(distance,0,100,0,5); 
Serial.println(value); 

 if(value==0)
   { digitalWrite(ledpin1,LOW);
     digitalWrite(ledpin2,LOW);
     digitalWrite(ledpin3,LOW);}
   if(value==1)
    {digitalWrite(ledpin1,LOW);
     digitalWrite(ledpin2,LOW);
     digitalWrite(ledpin3,HIGH);}
   if(value==2)
    {digitalWrite(ledpin1,LOW);
    digitalWrite(ledpin2,HIGH);
    digitalWrite(ledpin3,LOW);}
    if(value==3)
   { digitalWrite(ledpin1,LOW);
    digitalWrite(ledpin2,HIGH);
    digitalWrite(ledpin3,HIGH);}
     if(value==4)
   { digitalWrite(ledpin1,HIGH);
    digitalWrite(ledpin2,LOW);
    digitalWrite(ledpin3,LOW);}
     if(value==5)
   { digitalWrite(ledpin1,HIGH);
    digitalWrite(ledpin2,LOW);
    digitalWrite(ledpin3,HIGH);}
  }
  lastButton = currentButton;
  
  digitalWrite(ledpin1,LOW);
  digitalWrite(ledpin2,LOW);
  digitalWrite(ledpin3,LOW);
  

}
