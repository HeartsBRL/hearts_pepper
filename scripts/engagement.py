#!/usr/bin/env python

from pepper_controller import PepperController

import numpy
import time

robotIP = "westey.local" #Stevey
PORT = 9559

class Engagement(PepperController):

    def seePeople(self):
        while True:
            print self.memoryProxy.getData("EngagementZones/PeopleInZone1")
            time.sleep(2)

if __name__ == '__main__':
    task = Engagement(robotIP, PORT)
    task.seePeople()
