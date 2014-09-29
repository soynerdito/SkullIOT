
 
#include "TimerOne.h"

int rightRed = A2;
int rightWhite = A1;
int leftRed = A3;
int leftWhite = A0;

int rightEye[] = { rightRed, rightWhite };
int leftEye[]  = { leftRed,  leftWhite  };

int incomingByte = 0;   // for incoming serial data
String inData;
int sleepCount=0;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode( rightEye[0], OUTPUT );
  pinMode( rightEye[1], OUTPUT );     
  pinMode( leftEye[0],  OUTPUT );     
  pinMode( leftEye[1],  OUTPUT );
  
  //Initialize Serial Communication
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  
  //Init Timer for inactivity
  Timer1.initialize(1000000);         // initialize timer1, and set a 1 second period
  Timer1.attachInterrupt(callback);  // attaches callback() as a timer overflow interrupt
  
}

int shortTime = 350;
void doLevel( int port1, int port2, int level ){
  digitalWrite(port1, level);
  digitalWrite(port2, level);
}
// the loop routine runs over and over again forever:
void loop(){ 
  
  readLine();
  
  if( sleepCount == 30 ){
    doBlinkEye( rightEye, 3 );
    delay(500);
    doBlinkEye( leftEye, 3 );
    sleepCount = 0;
  }

}


void doBlinkEye(int eye[], int len){  
  allOff();
  int time = 0;
  while( time++ < len ){
    doLevel( eye[0], eye[1], HIGH );
    delay(50);
    allOff();
    delay(50);
  }
}

void allOff(){
  doLevel(  rightEye[0], rightEye[1], LOW );
  doLevel(  leftEye[0], leftEye[1], LOW );
}

boolean readingMessage = false;
boolean readLine(){
  while (Serial.available() > 0)
  {
      char recieved = Serial.read();
      if( recieved == '|' ){
        readingMessage = true;
        inData = "";
      }
      if( readingMessage && recieved!= 10 && recieved != 13 && recieved != '|'){
        inData += recieved;
      }

      // Process message when new line character is recieved
      if (readingMessage && (recieved == 13 || recieved == 10 ))
      {
          readingMessage = false;
          onCommandReceived(inData);
          inData = "";
          readingMessage = false;
          return true;
      }
  }
  return false;
}


void onCommandReceived(String command){
  if( command == "BR" ){
    doBlinkEye( rightEye, 3 );
    delay(20);
    allOff();
  }else if( command == "BL" ){
    doBlinkEye( leftEye, 3 );
    delay(20);
    allOff();
  }else if( command == "SKULL" ){
    Serial.println("MASTER");
  }
  if( sleepCount > -32,768 ){
    sleepCount--;    
  }  
}


void callback()
{
  sleepCount++;  
}



