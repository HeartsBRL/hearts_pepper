#!/usr/bin/env python

from pepper_controller import PepperController

import numpy
import Image

robotIP = "10.2.0.110" #Stevey
PORT = 9559

class LiftTask(PepperController):

    def toStart(self):


    def toLift(self):
          
         
    def toEnd(self):
        

if __name__ == '__main__':
    liftTask = LiftTask(robotIP, PORT)
    
