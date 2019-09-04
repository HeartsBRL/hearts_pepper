#!/usr/bin/env python

from pepper_controller import PepperController

import numpy
import Image
import time

robotIP = "10.2.0.112" #Stevey
PORT = 9559

class ManualLoc(PepperController):

    def startingVariables(self):
        ## Verbal confirmation it's starting
        self.say("boop")
        ## Turn of auto-interaction features
        self.lifeProxy.setState("safeguard")
        ## Set how close Pepper is allowed to get to obstacles
        self.motionProxy.setTangentialSecurityDistance(0.03)
        self.motionProxy.setOrthogonalSecurityDistance(0.1)

    def printLoc(self):
        print(self.navigationProxy.getRobotPositionInMap())

    def goHere(self,x,y,t):
        ret = self.navigationProxy.navigateToInMap((x,y,t))
        print ret
        if ret == 0:
            self.say("I made it!")
        else:
            self.say("Sorry, I couldn't get there.")
            

if __name__ == '__main__':
    task = ManualLoc(robotIP, PORT)
    task.startingVariables()
    while True:
        time.sleep(5)
        task.printLoc()
    #task.goHere(0,0,0)
