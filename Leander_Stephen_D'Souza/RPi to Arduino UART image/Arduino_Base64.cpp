#include <stdlib.h>

void setup()
{
Serial.begin(115200);

}


void loop()
{

START:
  
if (Serial.available()>0)
{  i++;
   
  char ch= Serial.read();
   if (ch=='\n')
     { Serial.print("\\n");
       goto START;} 

  
  if( ch >= '0' && ch <= '9' )
{
    int j=ch-'0';
    Serial.print(j);
    
   
    
}

  else
   { 
    
    Serial.print(ch);
      }
    

}



}
