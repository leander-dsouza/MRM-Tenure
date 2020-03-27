const int ledpin=13;
int ledstate=LOW;
const int buttonpin=5;
boolean buttonstate=LOW;
int count=0; 

void setup() {
  // put your setup code here, to run once:
pinMode(buttonpin,INPUT);
pinMode(ledpin,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
if(debounce(buttonstate)==HIGH&&buttonstate==LOW)
{  count++;
   buttonstate=HIGH; }
   else
   if(debounce(buttonstate)==LOW&&buttonstate==HIGH)
   buttonstate=LOW;
   {if(count%2==1)
   digitalWrite(ledpin,HIGH);
   else
    digitalWrite(ledpin,LOW);}
}

boolean debounce(boolean buttonstate)
{
   boolean nowstate=digitalRead(buttonpin);
   if(buttonstate!=nowstate)
   {   delay(10);
       nowstate=digitalRead(buttonpin);}
       return nowstate;
}
