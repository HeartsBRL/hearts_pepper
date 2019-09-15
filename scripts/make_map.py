#!/usr/bin/env python

from pepper_controller import PepperController

import numpy

# pip install pillow
try:
    from PIL import Image
except ImportError:
    import Image

robotIP = "westey.local" #Stevey
PORT = 9559

class MakeMap(PepperController):

    def startingVariables(self):
        ## Verbal confirmation it's starting
        self.say("boop")
        ## Turn of auto-interaction features
        # self.lifeProxy.setState("solitary")
        self.lifeProxy.setState("safeguard")
        ## Set how close Pepper is allowed to get to obstacles
        self.motionProxy.setTangentialSecurityDistance(0.01)
        self.motionProxy.setOrthogonalSecurityDistance(0.05)

    def explore(self,r):
        ## SLAM in a radius of r metres
        self.say("I'm going to have a look around.")
        ret = self.navigationProxy.explore(r)
        if ret != 0:
            print "Exploration failed :("
            self.say("Oops, something went wrong. Sorry!")

        else:
            print "Exploration success!"
            self.say("I'm done exploring!")

        ## Save the map ##
        # TODO write the path to a file for later use?
        path = self.navigationProxy.saveExploration()
        print "saved at: " + path

        ## start the localization routine so the Pepper can navigate
        self.navigationProxy.startLocalization()
        print "Started localization"

        ## Gets the generated map from the robot and displays it on the screen ##
        arrMap = self.navigationProxy.getMetricalMap()
        map_width = arrMap[1]
        map_height = arrMap[2]
        img = numpy.array(arrMap[4]).reshape(map_width, map_height)
        img = (100 - img) * 2.55 # from 0..100 to 255..0
        img = numpy.array(img, numpy.uint8)
        Image.frombuffer('L',  (map_width, map_height), img, 'raw', 'L', 0, 1).show()

        print "Returning to origin"
        self.say("I'm heading back to the origin.")
        ret = self.goHere(0,0,0)
        print ret


if __name__ == '__main__':
    task = MakeMap(robotIP, PORT)
    task.explore(2)
    #task.goHere(1,-1,0)
    task.say('Remember to update the map path in reload_map.py so you don\'t load an old map!')
