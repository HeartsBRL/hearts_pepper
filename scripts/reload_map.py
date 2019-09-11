#!/usr/bin/env python

from pepper_controller import PepperController


import time

robotIP = "10.2.0.111" #Stevey
PORT = 9559

class MapLoad(PepperController):

    def reloadMap(self):
        self.mapLoc = "/home/nao/.local/share/Explorer/2014-04-04T032006.413Z.explo"
        self.navigationProxy.stopLocalization()
        ### Update this with new path when you make a new map """
        self.navigationProxy.loadExploration(self.mapLoc)
        print("Loaded map from " + self.mapLoc)


if __name__ == '__main__':
    task = MapLoad(robotIP, PORT)
    task.reloadMap()
