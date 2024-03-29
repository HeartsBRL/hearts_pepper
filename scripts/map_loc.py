#!/usr/bin/env python

from pepper_controller import PepperController


import time

robotIP = "westey.local" #Stevey
PORT = 9559

class MapLoc(PepperController):

    def printLoc(self):
        print("Map, World")
        print(self.navigationProxy.getRobotPositionInMap()[0],self.motionProxy.getRobotPosition(True))
        #print("World:")
        #print(self.motionProxy.getRobotPosition(True)[0:2])


if __name__ == '__main__':
    task = MapLoc(robotIP, PORT)
    task.navigationProxy.startLocalization()
    while True:
        time.sleep(5)
        task.printLoc()
    #task.goHere(0,0,0)
