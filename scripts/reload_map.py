#!/usr/bin/env python

from pepper_controller import PepperController


import time

robotIP = "westey.local" #Stevey
PORT = 9559

class MapLoad(PepperController):

    #Map orogin is 3.43m from the right wall
    def reloadMap(self):
        self.mapLoc = "/home/nao/.local/share/Explorer/2019-09-17T171412.382Z.explo"
        self.navigationProxy.stopLocalization()
        ### Update this with new path when you make a new map """
        self.navigationProxy.loadExploration(self.mapLoc)
        print("Loaded map from " + self.mapLoc)
        self.navigationProxy.startLocalization()
        


if __name__ == '__main__':
    task = MapLoad(robotIP, PORT)
    task.reloadMap()
