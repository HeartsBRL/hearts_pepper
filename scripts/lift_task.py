#!/usr/bin/env python

from pepper_controller import PepperController

import numpy
import Image

robotIP = "10.2.0.114" #Stevey
PORT = 9559

class LiftTask(PepperController):

    def toStart(self):
        self.navigationProxy.navigateToInMap((0,-1,0))
        
    def toLift(self):
        self.navigationProxy.navigateToInMap((0,0,0))  
         
    def toEnd(self):
        self.navigationProxy.navigateToInMap((0,1,0))

if __name__ == '__main__':
    liftTask = LiftTask(robotIP, PORT)
    liftTask.toStart()
    #liftTask.toLift()
    #liftTask.toEnd()
