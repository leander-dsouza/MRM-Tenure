
const int ledpin1=13;
const int ledpin2=2;
const int ledpin3=3;
int ledstate1=LOW;
int ledstate2=LOW;
int ledstate3=LOW;
const int buttonpin=8;
boolean buttonstate=LOW;
int count=0; 

void setup() {
  // put your setup code here, to run once:
pinMode(buttonpin,INPUT);
pinMode(ledpin1,OUTPUT);
pinMode(ledpin2,OUTPUT);
pinMode(ledpin3,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
if(debounce(buttonstate)==HIGH&&buttonstate==LOW)
{  count++;
   buttonstate=HIGH; }
   else
   if(debounce(buttonstate)==LOW&&buttonstate==HIGH)
   buttonstate=LOW;
   
   
   
   if(count%8==1)
   { digitalWrite(ledpin1,LOW);
     digitalWrite(ledpin2,LOW);
     digitalWrite(ledpin3,LOW);}
   if(count%8==2)
    {digitalWrite(ledpin1,LOW);
     digitalWrite(ledpin2,LOW);
     digitalWrite(ledpin3,HIGH);}
   if(count%8==3)
    {digitalWrite(ledpin1,LOW);
    digitalWrite(ledpin2,HIGH);
    digitalWrite(ledpin3,LOW);}
    if(count%8==4)
   { digitalWrite(ledpin1,LOW);
    digitalWrite(ledpin2,HIGH);
    digitalWrite(ledpin3,HIGH);}
     if(count%8==5)
   { digitalWrite(ledpin1,HIGH);
    digitalWrite(ledpin2,LOW);
    digitalWrite(ledpin3,LOW);}
      if(count%8==6)
   { digitalWrite(ledpin1,HIGH);
    digitalWrite(ledpin2,LOW);
    digitalWrite(ledpin3,HIGH);}
      if(count%8==7)
   { digitalWrite(ledpin1,HIGH);
    digitalWrite(ledpin2,HIGH);
    digitalWrite(ledpin3,LOW);}
      if(count%8==0)
   { digitalWrite(ledpin1,HIGH);
    digitalWrite(ledpin2,HIGH);
    digitalWrite(ledpin3,HIGH);}
    
    
}

boolean debounce(boolean buttonstate)
{
   boolean nowstate=digitalRead(buttonpin);
   if(buttonstate!=nowstate)
   {   delay(10);
       nowstate=digitalRead(buttonpin);}
       return nowstate;
}
