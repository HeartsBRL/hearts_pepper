#!/usr/bin/env python

from pepper_controller import PepperController
import time
import qi
from naoqi import ALModule, ALBroker

robotIP = "10.2.0.111" #Stevey
PORT = 9559

class PeoplePerception(PepperController):

    def whosThere(self):
        # memoryProxy.subscribeToEvent("VisiblePeopleList", "peoplemodule", "peoplecallback")
        self.peoplePerceptionProxy.resetPopulation()
        self.peopleSubscriber = self.memoryService.subscriber("PeoplePerception/VisiblePeopleList")
        self.peopleSubscriber.signal.connect(self.onPeeps)
        print "Connected"
        #time.sleep(30)
        self.peopleSubscriber.signal.disconnect(self.onPeeps)
        print "Disconnected"


    def onPeeps(self, value):
        print "hey!"
        print value
        if len(value) > 0:
            for id in value:
                print self.memoryProxy.getData("PeoplePerception/Person/" + str(id) + "/PositionInWorldFrame")

if __name__ == '__main__':
    pper = PeoplePerception(robotIP, PORT)
    # broker = ALBroker("pythonBroker","10.2.0.222",0,robotIP,PORT)
    # what = thingy("peoplemodule")

    pper.whosThere()
    while True:
        pass

    #while loop keeps script alive for the threads to run. Super bad but
    #can change for the real thing.
    #x = 1
    #while (True):
    #    y= x + 1
