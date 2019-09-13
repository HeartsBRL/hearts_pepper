#!/usr/bin/env python

from pepper_controller import PepperController


import time

robotIP = "stevey.local" #Stevey
PORT = 9559

class Relocalise(PepperController):

    def printLoc(self):
        self.navigationProxy.relocalizeInMap([0,0,0])


if __name__ == '__main__':
    task = Relocalise(robotIP, PORT)
    task.navigationProxy.startLocalization()
    while True:
        time.sleep(5)
        task.printLoc()
    #task.goHere(0,0,0)
