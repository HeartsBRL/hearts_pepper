#!/usr/bin/env python

from pepper_controller import PepperController

import numpy
import Image
import thread
import time
import json

robotIP = "stevey.local" #Stevey
PORT = 9559

class NavTest(PepperController):

    # def setup2(self):
    #     #enbles localisation and navigation
    #     self.navigationProxy.startLocalization()
    #     ## Turn off auto-interaction features
    #     self.lifeProxy.setState("solitary")
    #     ## Set how close Pepper is allowed to get to obstacles
    #     self.motionProxy.setTangentialSecurityDistance(0.01)
    #     self.motionProxy.setOrthogonalSecurityDistance(0.1)


        # *args allows any number of arguments
    def stopMove(self,*args):
        #wait for pepper to get part way through the previous movement command,
        #stop the movement, then resume it
        time.sleep(8)
        self.say("Stopping!")
        self.navigationProxy.stopExploration() #Stops pepper navigating
        time.sleep(8)
        self.goHere(*self.going)

    def load_dict(self):
        #loads a dictionary from the locations json file
        json_name = 'locations.json'

        with open(json_name) as json_data:
            self.locations = json.load(json_data)

        print("using locations file: " + json_name)

    def run_through(self):

        self.navigationProxy.startLocalization()
        self.goHere(*self.locations["start"][1])
        #self.goHere(*self.locations["outside door"][1])
        #self.goHere(*self.locations["inside door"][1])
        #self.goHere(*self.locations["lift back"][1])
        #self.goHere(*self.locations["inside door"][1])
        #self.goHere(*self.locations["outside door"][1])
        #self.goHere(*self.locations["finish"][1])
        print('Finished run through')


if __name__ == '__main__':
    navTest = NavTest(robotIP, PORT)
    # navTest.setup2()
    navTest.load_dict()
    navTest.run_through()

    #while loop keeps script alive for the threads to run. Super bad but
    #can change for the real thing.
    #x = 1
    #while (True):
    #    y= x + 1
