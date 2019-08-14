#!/usr/bin/env python

from pepper_controller import PepperController

import numpy
import Image

robotIP = "10.2.0.110" #Stevey
PORT = 9559

class DummyTask(PepperController):

    def work(self):
        #self.say("boop")
        self.lifeProxy.setState("safeguard")
        self.motionProxy.setTangentialSecurityDistance(0.03)
        self.motionProxy.setOrthogonalSecurityDistance(0.1)
        """
        ret = self.navigationProxy.explore(3)
        if ret != 0:
            print "Exploration failed :("
            self.say("Oops, something went wrong. Sorry!")
                            
        else:
            print "Exploration success!"
            self.say("I'm done exploring!")
        
        path = self.navigationProxy.saveExploration()
        print "saved at: " + path

        self.navigationProxy.stopLocalization()
        self.navigationProxy.startLocalization()
        print "Started localization"

        arrMap = self.navigationProxy.getMetricalMap()
        map_width = arrMap[1]
        map_height = arrMap[2]
        img = numpy.array(arrMap[4]).reshape(map_width, map_height)
        img = (100 - img) * 2.55 # from 0..100 to 255..0
        img = numpy.array(img, numpy.uint8)
        Image.frombuffer('L',  (map_width, map_height), img, 'raw', 'L', 0, 1).show()

        print "Returning to origin"
        """
        ret = self.navigationProxy.navigateToInMap((1,-1,0))
        print ret
            

if __name__ == '__main__':
    dummy = DummyTask(robotIP, PORT)
    dummy.work()
