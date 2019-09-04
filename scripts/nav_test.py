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
        self.goHere(-1.34,-0.82,0)
        self.goHere(0.1,0.55,0)
        self.goHere(-0.1,0.11,0)
        self.goHere(-0.25,1.17,0)
        self.goHere(-0.1,0.11,0)
        self.goHere(0.1,0.55,0)
        self.goHere(1.17,-0.2,0)
    

if __name__ == '__main__':
    navTest = NavTest(robotIP, PORT)
    #navTest.load_dict()
    navTest.run_through()
    
    #while loop keeps script alive for the threads to run. Super bad but
    #can change for the real thing.
    x = 1
    while (True):
        y= x + 1
