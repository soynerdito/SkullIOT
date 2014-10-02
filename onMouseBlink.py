import paho.mqtt.client as mqtt
import json
import urllib2
import time
import win32gui, win32con, win32api
from ctypes import *
user32 = windll.user32
import thread
from ctypes import wintypes

from Queue import Queue
import threading
from time import sleep


class KeyboardHook:
   """
   To install the hook, call the (gasp!) installHook() function.
   installHook() takes a pointer to the function that will be called
   after a keyboard event.  installHook() returns True if everything
   was successful, and False if it failed
   Note:  I've also provided a function to return a valid function pointer
   
   To make sure the hook is actually doing what you want, call the
   keepAlive() function
   Note:  keepAlive() doesn't return until kbHook is None, so it should
   be called from a separate thread
   
   To uninstall the hook, call uninstallHook()
   
   Note:  relies on modules provided by pywin32.
   http://sourceforge.net/projects/pywin32/
   """
   def __init__(self):
      self.user32     = windll.user32
      self.kbHook     = None
      
   def installHook(self, pointer):
      self.kbHook = self.user32.SetWindowsHookExA(
         win32con.WH_KEYBOARD_LL,
         pointer,
         win32api.GetModuleHandle(None),
         0 # this specifies that the hook is pertinent to all threads
      )
      if not self.kbHook:
         return False
      return True
      
   def keepAlive(self):
      if self.kbHook is None:
         return
      msg = win32gui.GetMessage(None, 0, 0)
      while msg and self.kbHook is not None:
         win32gui.TranslateMessage(byref(msg))
         win32gui.DispatchMessage(byref(msg))
         msg = win32gui.GetMessage(None, 0, 0)
         
   def uninstallHook(self):
      if self.kbHook is None:
         return
      self.user32.UnhookWindowsHookEx(self.kbHook)
      self.kbHook = None
      
      
class MouseHook:
   """
   
   """
   def __init__(self):
      self.user32     = windll.user32
      self.msHook     = None
      
   def installHook(self, pointer):
      self.msHook = self.user32.SetWindowsHookExA(
         win32con.WH_MOUSE_LL,
         pointer,
         win32api.GetModuleHandle(None),
         0 # this specifies that the hook is pertinent to all threads
      )
      if not self.msHook:
         return False
      return True
      
   def keepAlive(self):
      if self.msHook is None:
         return
      msg = win32gui.GetMessage(None, 0, 0)
      while msg and self.msHook is not None:
         win32gui.TranslateMessage(byref(msg))
         win32gui.DispatchMessage(byref(msg))
         msg = win32gui.GetMessage(None, 0, 0)
         
   def uninstallHook(self):
      if self.msHook is None:
         return
      self.user32.UnhookWindowsHookEx(self.msHook)
      self.msHook = None
      
      
##################################################
# returns a function pointer to the fn paramater #
# assumes the function takes three params:       #
# c_int, c_int, and POINTER(c_void_p)            #
##################################################
def getFunctionPointer(fn):
   CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
   return CMPFUNC(fn)
   
   
#############################################
# function to handle keyboard events        #
#############################################
def kbEvent(nCode, wParam, lParam):
   if wParam is not win32con.WM_KEYDOWN: 
      return user32.CallNextHookEx(keyboardHook.kbHook, nCode, wParam, lParam)
   print chr(lParam[0])
   return user32.CallNextHookEx(keyboardHook.kbHook, nCode, wParam, lParam)
   
   
def msEvent(nCode, wParam, lParam):
   if nCode is not win32con.HC_ACTION: 
      #print 'Event detect!'
   
      return user32.CallNextHookEx(mouseHook.msHook, nCode, wParam, lParam)
   if wParam == win32con.WM_LBUTTONDOWN:
      postLeftBlink()
   elif wParam == win32con.WM_RBUTTONDOWN:
      postRightBlink()
   return user32.CallNextHookEx(mouseHook.msHook, nCode, wParam, lParam)
   
keyboardHook = None
mouseHook = None

def test_kbhook():
   global keyboardHook
   keyboardHook = KeyboardHook()
   pointer = getFunctionPointer(kbEvent)
   if keyboardHook.installHook(pointer):
      print "installed hook"
      #keyboardHook.uninstallHook()
      #print "removed hook"
   keyboardHook.keepAlive()
   
def test_mshook():
   global mouseHook
   mouseHook = MouseHook()
   pointer = getFunctionPointer(msEvent)
   if mouseHook.installHook(pointer):
      print "installed hook"
      #keyboardHook.uninstallHook()
      #print "removed hook"
   mouseHook.keepAlive()

def postLeftBlink():
    #q.put( '{"cmd": "BL"}' )
    q.put( {'cmd':'BL'} )
    print 'LClick'
    #q.join()

def postRightBlink():
    #q.put( '{"cmd": "BR"}' )
    q.put( {'cmd':'BR'} )
    #q.join()

#Queue of messages to post
q = Queue()

def post( data ): 
    #data = {'cmd':'BR'}
    data = json.dumps(data)
     
    url = 'http://remote-alert.herokuapp.com/skull'
     
    req = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Accept': 'application/json'})

    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
    except Exception:
        pass

class MyWorker:
    def __init__(self):
        #self.client = mqtt.Client()
        #self.client.connect("iot.eclipse.org", 1883, 60)
        t = threading.Thread(target=self.worker)
        t.daemon = True
        t.start()

    def worker(self):
        name = threading.currentThread().getName()
        print "Thread %s started" % name
        #Connecto to MQTT Broker server        
        while True:
            item = q.get()            
            #self.client.publish("office_skull", item , 1)
            #self.client.disconnect()
            post( item )
            print 'Publishing msg'
            sleep(1)
            q.task_done()


if __name__ == '__main__':
   #Worker is in charge of posting the messages
   worker = MyWorker()
   test_mshook()
   
   print "Workers started"
   
   
   
   
   raw_input()
