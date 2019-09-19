#!/usr/bin/env python

from pepper_controller import PepperController


import time

robotIP = "westey.local"
PORT = 9559

class MapLoc(PepperController):

    def doIt(self):
        self.lifeProxy.setState("solitary")
        self.speechRecognition()

if __name__ == '__main__':
    task = MapLoc(robotIP, PORT)
    task.doIt()
    #task.goHere(0,0,0)
