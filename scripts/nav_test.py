#!/usr/bin/env python

from pepper_controller import PepperController

import numpy
import Image
import thread
import time

robotIP = "10.2.0.114" #Stevey
PORT = 9559

class NavTest(PepperController):

    def setup2(self):
        #enbles localisation and navigation
        self.navigationProxy.startLocalization()

    def toStart(self): 
        #Send pepper to a pre-defined start location
        self.navigationProxy.navigateToInMap((0.4,0,0))
        self.navigationProxy.navigateToInMap((0.5,0,0))        
        
        # *args allows any number of arguments 
    def toEnd(self,*args):
        #send peper to the end locaiton
        self.say("Going to the end")
        ret = self.navigationProxy.navigateToInMap((-1,0,0))
        print "toEnd: " + str(ret)

        # *args allows any number of arguments
    def stopMove(self,*args):
        #wait for pepper to get part way through the previous movement command,
        #stop the movement, then resume it
        time.sleep(8)
        self.say("Stopping!")        
        self.navigationProxy.stopExploration() #Stops pepper navigating
        time.sleep(6)
        self.toEnd()

    def test(self):
        #Start the thread to send pepper to the end location  
        thread.start_new_thread(self.toEnd,(self,1))
        #Start thread to interrupt pepper's movement
        thread.start_new_thread(self.stopMove,(self,1))

    

if __name__ == '__main__':
    navTest = NavTest(robotIP, PORT)
    navTest.setup2()
    navTest.toStart()
    navTest.test()
    #while loop keeps script alive for the threads to run. Super bad but
    #can change for the real thing.
    x = 1
    while (True):
        y= x + 1
