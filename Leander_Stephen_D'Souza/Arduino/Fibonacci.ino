const int ledpin=A5;
int ledstate=LOW;
const int buttonpin=2;
boolean buttonstate=LOW;
int count=0; 
int first=0;
int second=1;
int next;

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
   
   if(count%2==1)
   { for (int j=0;j<256;j++)
   {
      if (j<=1)
        { next=j;
          analogWrite(ledpin,next);}
      else
      {
         next=first+second;
         first=second;
         second=next;
         analogWrite(ledpin,next);}
      
   }
    }
   else
    analogWrite(ledpin,0);
}

boolean debounce(boolean buttonstate)
{
   boolean nowstate=digitalRead(buttonpin);
   if(buttonstate!=nowstate)
   {   delay(10);
       nowstate=digitalRead(buttonpin);}
       return nowstate;
}
