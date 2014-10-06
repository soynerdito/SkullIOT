/*
 Basic MQTT example 
 
  - connects to an MQTT server
  - publishes "hello world" to the topic "outTopic"
  - subscribes to the topic "inTopic"
*/

#include <Adafruit_CC3000.h>
#include <ccspi.h>
#include <SPI.h>
#include <PubSubClient.h>

 
#include "TimerOne.h"

int rightRed = A2;
int rightWhite = A1;
int leftRed = A3;
int leftWhite = A0;

int rightEye[] = { rightRed, rightWhite };
int leftEye[]  = { leftRed,  leftWhite  };


// These are the interrupt and control pins
#define ADAFRUIT_CC3000_IRQ   3  // MUST be an interrupt pin!
// These can be any two pins
#define ADAFRUIT_CC3000_VBAT  5
#define ADAFRUIT_CC3000_CS    10
// Use hardware SPI for the remaining pins
// On an UNO, SCK = 13, MISO = 12, and MOSI = 11
Adafruit_CC3000 cc3000 = Adafruit_CC3000(ADAFRUIT_CC3000_CS, ADAFRUIT_CC3000_IRQ, ADAFRUIT_CC3000_VBAT,
                                         SPI_CLOCK_DIVIDER); // you can change this clock speed but DI

#define WLAN_SSID       "SSID"        // cannot be longer than 32 characters!
#define WLAN_PASS       "password"
// Security can be WLAN_SEC_UNSEC, WLAN_SEC_WEP, WLAN_SEC_WPA or WLAN_SEC_WPA2
#define WLAN_SECURITY   WLAN_SEC_WPA2
//198.41.30.241
//byte server[] = { 172, 16, 0, 2 };
byte server[] = { 198, 41, 30, 241 };

PubSubClient client(server, 1883, callback, cc3000);


void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
  Serial.println(topic);
  payload[length] = '\0';
  String strPayload = String((char*)payload);

  //Serial.println(strPayload);
  //Parsing Command from JSON received
  int idxStart =   strPayload.indexOf("\"cmd\": \"");
  idxStart = idxStart + 8;
  int idxEnd =   strPayload.indexOf("\"", (idxStart+1) );
  String command = strPayload.substring( idxStart, idxEnd );
  onCommandReceived( command );
/*  if( command == "BL"){
    Serial.println("Blink Left");    
  }else if( command == "BR") {
    Serial.println("Blink Right");
  }*/
}

//Blink stuff
int shortTime = 350;
void doLevel( int port1, int port2, int level ){
  digitalWrite(port1, level);
  digitalWrite(port2, level);
}

void setup()
{
  // initialize the digital pin as an output.
  pinMode( rightEye[0], OUTPUT );
  pinMode( rightEye[1], OUTPUT );     
  pinMode( leftEye[0],  OUTPUT );     
  pinMode( leftEye[1],  OUTPUT );

#ifdef DEBUG_SERIAL  
  Serial.begin(115200);
#endif  
  cc3000.begin();

  if (!cc3000.deleteProfiles()) {
    while(1);
  }

  char *ssid = WLAN_SSID;             /* Max 32 chars */
  if (!cc3000.connectToAP(WLAN_SSID, WLAN_PASS, WLAN_SECURITY)) {
    while(1);
  }
   
  while (!cc3000.checkDHCP())
  {
    delay(100); // ToDo: Insert a DHCP timeout!
    doLevel(  rightEye[0], rightEye[1], HIGH );
  }
  doLevel(  rightEye[0], rightEye[1], LOW );

#ifdef DEBUG_SERIAL  
  Serial.println("Checking connection");
#endif  

  doConnectMqttStuff();
  
}

void doConnectMqttStuff(){
  if (client.connect("arduinoClient")) {    
#ifdef DEBUG_SERIAL      
    Serial.println("YES Connected");
#endif
    doLevel(  leftEye[0], rightEye[0], HIGH );
    //client.publish("outTopic","hello world");
    client.subscribe("office_skull");
    allOff();
  }else{    
#ifdef DEBUG_SERIAL            
    Serial.println("Not Connected");
#endif    
  } 
  doLevel(  leftEye[1], rightEye[1], HIGH );
}

void loop()
{  
  client.loop();
  if( !client.connected() ){
    digitalWrite(rightEye[1], HIGH);
    digitalWrite(leftEye[1], HIGH);
    doConnectMqttStuff();    
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


void onCommandReceived(String command){
  if( command == "BR" ){
    doBlinkEye( rightEye, 3 );
    delay(20);    
    allOff();
#ifdef DEBUG_SERIAL    
    Serial.println("RIGHT");
#endif    
  }else if( command == "BL" ){
    doBlinkEye( leftEye, 3 );
    delay(20);
    allOff();
#ifdef DEBUG_SERIAL    
    Serial.println("LEFT");
#endif
  }else if( command == "SKULL" ){
#ifdef DEBUG_SERIAL
    Serial.println("MASTER");
#endif
  }
  /*if( sleepCount > -32,768 ){
    sleepCount--;    
  }*/  
}
void allOff(){
  doLevel(  rightEye[0], rightEye[1], LOW );
  doLevel(  leftEye[0], leftEye[1], LOW );
}
