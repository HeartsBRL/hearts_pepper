#!/usr/bin/env python

from pepper_controller import PepperController

import numpy
import time

robotIP = "10.2.0.111" #Stevey
PORT = 9559

class ManualLoc(PepperController):

    def printLoc(self):
        print(self.navigationProxy.getRobotPositionInMap())


if __name__ == '__main__':
    task = ManualLoc(robotIP, PORT)
    task.navigationProxy.startLocalization()
    while True:
        time.sleep(5)
        task.printLoc()
    #task.goHere(0,0,0)
