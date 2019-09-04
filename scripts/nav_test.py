#!/usr/bin/env python

from pepper_controller import PepperController

import numpy
import Image
import thread
import time
import json

robotIP = "10.2.0.112" #Stevey
PORT = 9559

class NavTest(PepperController):

    def setup2(self):
        #enbles localisation and navigation
        self.navigationProxy.startLocalization()
    

        # *args allows any number of arguments
    def stopMove(self,*args):
        #wait for pepper to get part way through the previous movement command,
        #stop the movement, then resume it
        time.sleep(8)
        self.say("Stopping!")        
        self.navigationProxy.stopExploration() #Stops pepper navigating

    def load_dict(self):
        #loads a dictionary from the locations json file
        json_name = 'locations.json'
	
        with open(json_name) as json_data:
            self.locations = json.load(json_data)
	
        print("using locations file: " + json_name)

    def run_through(self):
        ## Turn of auto-interaction features
        self.lifeProxy.setState("solitary")
        ## Set how close Pepper is allowed to get to obstacles
        self.motionProxy.setTangentialSecurityDistance(0.01)
        self.motionProxy.setOrthogonalSecurityDistance(0.1)

        self.goHere(0.3,-1.9,0)
        self.goHere(0.5,-0.3,0)
        self.goHere(-0.28,0.19,0)
        self.goHere(-1.24,0.9,0)
        self.goHere(-0.28,0.19,0)
        self.goHere(0.5,-0.3,0)
        self.goHere(1.27,0.88,0)
    

if __name__ == '__main__':
    navTest = NavTest(robotIP, PORT)
    navTest.setup2()
    #navTest.load_dict()
    navTest.run_through()
    
    #while loop keeps script alive for the threads to run. Super bad but
    #can change for the real thing.
    #x = 1
    #while (True):
    #    y= x + 1
