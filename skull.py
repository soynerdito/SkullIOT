import io
import time
import sys
import serial

def send_and_receive( serPort, theinput, waitInSec ):
  serPort.write( theinput )  
  while True:
    try:
      time.sleep(waitInSec)
      state = serPort.readline()      
      return state
    except:
      print 'Exception'
      pass
  time.sleep(0.1)


#Manages skull device
class Skull:
    
    def __init__(self):
        self.client = 0
    
    #Simple wait after to allow Arduino to reset
    def connect(self, port):
        #'/dev/ttyACM0' 9600
        self.ser = serial.Serial(port, 9600, timeout=1 )        
    
    def isOnline(self):
        answer = send_and_receive(self.ser, '|SKULL\n|', 2)
        time.sleep(4)    
        if( answer.find('MASTER') != -1 ):
            return True
        return False
    
    def blinkRight(self):
        self.ser.write( '|BR\r' )
    
    def blinkLeft(self):
        self.ser.write( '|BL\n' )
  

if __name__ == "__main__":
    print('Testing out Skull')
    print('View Code for sample')
    mySkull = Skull()
    mySkull.connect('/dev/ttyACM0')
    if( mySkull.isOnline ):
        print 'ONLINE'
    else:
        print 'Offline'
    while True:
        mySkull.blinkRight()
        time.sleep(.5)
        mySkull.blinkLeft()
        time.sleep(.5)
