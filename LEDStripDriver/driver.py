# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 00:02:25 2015

@author: pi
"""


import RPi.GPIO as GPIO
from time import sleep
import SocketServer

RGB=None

def TakeAntiCode(data):
    if (data & 0x80) == 0:
        return 2
    elif (data & 0x40)==0:
        return 1
    else:
        return 0

class RGBLED:
    def __init__(self, datpin, clkpin):
        self.clk=clkpin
        self.dat=datpin
        self.color=[0, 0, 0, 0]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([self.dat, self.clk], GPIO.OUT, initial=0)

    
    def cleanup(self):
        GPIO.cleanup()

    def clkRise(self):
        GPIO.output(self.clk, 0)
        sleep(0.00002)
        GPIO.output(self.clk, 1)
        sleep(0.00002)
    
    def Send32Zero(self):
        for i in range(32):
            GPIO.output(self.dat,0)
            self.clkRise()
        
        
    def DatSend(self, dx):
        for i in range(32):
            if (dx&0x80000000):
                GPIO.output(self.dat, 1)
            else:
                GPIO.output(self.dat, 0)
            dx <<=1
            self.clkRise()
    
    def SetColorLow(self, red, green, blue):
        
        dx=0
        dx|=0x03<<30
        dx|=TakeAntiCode(blue)<<28
        dx|=TakeAntiCode(green)<<26
        dx|=TakeAntiCode(red)<<24
        dx|=blue<<16
        dx|=green<<8
        dx|=red
        self.Send32Zero()
        self.DatSend(dx)
        self.Send32Zero()
        
    def SetColor(self, red, green, blue, intensity=100):
        """red, green, blue, intensity are 0-100%"""
        self.color=[red, green, blue, intensity]
        cval=lambda x: int(255*x*intensity/10000)
        self.SetColorLow(cval(red), cval(green), cval(blue))
        
    def GetColor(self):
        return self.color
    
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global RGB
        self.request.settimeout(0.001)
        try:
            self.data=self.request.recv(1024).strip()
        except:
            return
        print self.data
        colors=[int(i) for i in self.data.split(",")]
        #print colors
        RGB.SetColor(colors[0], colors[1], colors[2], colors[3])
        #self.request.send(self.data)

    

if __name__=="__main__":
    RGB=RGBLED(11,13)
    server=SocketServer.TCPServer(("localhost", 5557), MyTCPHandler)
    try:
        server.serve_forever()
    except Exception as e:
        print e
        RGB.cleanup()
        server.server_close()
        
    finally:
        server.server_close()
        
    
    
    
#    driver=RGBLED(11,13)
#    try:
#        while True:
#            for i in [25, 50, 75, 100]:
#                driver.SetColor(100, 0, 0, i)
#                sleep(1)
#                driver.SetColor(100, 100, 0, i)
#                sleep(1)
#                driver.SetColor(100, 100, 100, i)
#                sleep(1)
#                driver.SetColor(0, 100, 100, i)
#                sleep(1)
#                driver.SetColor(0, 0, 100, i)
#                sleep(1)
#
#
#
#    except:    
#        driver.cleanup()
