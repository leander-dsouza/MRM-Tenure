//LEFT MOTOR
const int lback=1;
const int lfwd=2;
const int enA=3;
int speedA=0;

//LEFT REAR MOTOR                      
const int lrearback=1;                 
const int lrearfwd=2;                   

//RIGHT MOTOR
const int rback=4;
const int rfwd=5;
const int enB=6;
int speedB=0;

//RIGHT REAR MOTOR
const int rrearback=4;
const int rrearfwd=5;


//JOYSTICK
const int xAxis=A0;
const int yAxis=A1;
int x=512;
int y=512;


void setup() {
  // put your setup code here, to run once:
  pinMode(lback,OUTPUT);
  pinMode(lfwd,OUTPUT);
  pinMode(lrearback,OUTPUT);  //extra line for four wheeled bot
  pinMode(lrearfwd,OUTPUT);   //extra line for four wheeled bot
  pinMode(enA,OUTPUT);
  pinMode(rback,OUTPUT);
  pinMode(rfwd,OUTPUT);
  pinMode(rrearback,OUTPUT);   //extra line for four wheeled bot
  pinMode(rrearfwd,OUTPUT);    //extra line for four wheeled bot
  pinMode(enB,OUTPUT);
  pinMode(xAxis,INPUT);
  pinMode(yAxis,INPUT);
  Serial.begin(9600);

  digitalWrite(lfwd,LOW);
  digitalWrite(lback,LOW);
  digitalWrite(lrearfwd,LOW); //extra line for four wheeled bot
  digitalWrite(lrearback,LOW); //extra line for four wheeled bot
  digitalWrite(rfwd,LOW);
  digitalWrite(rback,LOW);
  digitalWrite(rrearfwd,LOW);//extra line for four wheeled bot
  digitalWrite(rrearback,LOW);//extra line for four wheeled bot
  digitalWrite(enA,LOW);
  digitalWrite(enB,LOW);
 

}

void loop() {
  // put your main code here, to run repeatedly:

x=analogRead(xAxis);
x=x-9;
y=analogRead(yAxis);


//Serial.print("X = ");
//Serial.print(x+'\t');
//Serial.print("  Y = ");
//Serial.println(y);

//QUAD 1
    if((x<=512)&&((y>=512)&&(y<=1023)))
{ 
      if((x+y)>=1023) //OCT1
        oct1(x,y);
        
      if((x+y)<1023) //OCT2
        oct2(x,y);
        
}
//QUAD 2
    if((x<=512)&&(y<=512))
{ 
      if((x-y)<=0) //OCT3
        oct3(x,y);
        
     if((x-y)>0) //OCT4
        oct4(x,y);
        
}
//QUAD 3
    if(((x>=512)&&(x<=1023))&&(y<=512))
{ 
      
      if((x+y)<=1023) //OCT5
        oct5(x,y);
        
      if((x+y)>1023) //OCT6
        oct6(x,y);
        
}
//QUAD 4
    if(((x>=512)&&(x<=1023))&&((y>=512)&&(y<=1023)))
{ 
     if((y-x)<=0) //OCT7
        oct7(x,y);
        
     if((y-x)>0) //OCT8
        oct8(x,y);
        
}

}

   void leftF(int speedA)
   {
      digitalWrite(lfwd,HIGH);
      digitalWrite(lback,LOW);
      digitalWrite(lrearfwd,HIGH); //extra line for four wheeled bot
      digitalWrite(lrearback,LOW); //extra line for four wheeled bot
      analogWrite(enA,speedA);
      Serial.print("leftF = ");
      Serial.print(speedA+'\t');
      }
      
   void leftB(int speedA)
   {
      digitalWrite(lfwd,LOW);
      digitalWrite(lback,HIGH);
      digitalWrite(lrearfwd,LOW); //extra line for four wheeled bot
      digitalWrite(lrearback,HIGH);//extra line for four wheeled bot
      analogWrite(enA,speedA);
      Serial.print("leftB = ");
      Serial.print(speedA+'\t');
      }

   void rightF(int speedB)
   {
      digitalWrite(rfwd,HIGH);
      digitalWrite(rback,LOW);
      digitalWrite(rrearfwd,HIGH);//extra line for four wheeled bot
      digitalWrite(rrearback,LOW);//extra line for four wheeled bot
      analogWrite(enB,speedB);
      Serial.print("  rightF = ");
      Serial.println(speedB);
      } 
       
   void rightB(int speedB)
   {
      digitalWrite(rfwd,LOW);
      digitalWrite(rback,HIGH);
      digitalWrite(rrearfwd,LOW);//extra line for four wheeled bot
      digitalWrite(rrearback,HIGH);//extra line for four wheeled bot
      analogWrite(enB,speedB);
      Serial.print("  rightB = ");
      Serial.println(speedB);
      }  
      
  
    
    
    void oct1(int x,int y)
    {
      speedA=map(y,1023,512,255,0)-12;  //axis wise independent
      speedB=map(x+y,1535,1023,255,0); 

      leftF(speedA);
      rightF(speedB);

     }

   void oct2(int x,int y)
    {
     
      speedA=map(x,512,0,0,255)-12;
      speedB=map(x+y,1023,512,0,255);

      leftF(speedA);
      rightB(speedB);

     }
     
  void oct3(int x,int y)             //switching apparent oct6
    {
      speedA=map(y-x,512,0,255,0)-12;
      speedB=map(x,512,0,0,255);
     
      leftF(speedA);
      rightB(speedB);

     }

 void oct4(int x,int y)
    {
     
      speedA=map(x-y,512,0,255,0)-12;
      speedB=map(y,512,0,0,255);

      leftB(speedA);
      rightB(speedB);

     }

 void oct5(int x,int y)
    {
      speedA=map(y,512,0,0,255)-12;
      speedB=map(x+y,1023,512,0,255);

      leftB(speedA);
      rightB(speedB);

     }
 
 void oct6(int x,int y)                   //switching apparent oct3
    {
      speedA=map(x,1023,512,255,0)-12;
      speedB=map(x+y,1535,1023,255,0);

      leftB(speedA);
      rightF(speedB);

     }


 void oct7(int x,int y)   
    {
      speedA=map(x-y,0,512,0,255)-12;
      speedB=map(x,1023,512,255,0);

      leftB(speedA);
      rightF(speedB);

     }

 void oct8(int x,int y)   
    {
      speedA=map(y-x,0,512,0,255)-12;
      speedB=map(y,1023,512,255,0);

      leftF(speedA);
      rightF(speedB);

     }
