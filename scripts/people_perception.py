#!/usr/bin/env python

from pepper_controller import PepperController
import time
import qi
from naoqi import ALModule
import json
import thread

robotIP = "stevey.local" #Stevey
PORT = 9559

class PeoplePerception(PepperController):

    def whosThere(self):
        # memoryProxy.subscribeToEvent("VisiblePeopleList", "peoplemodule", "peoplecallback")
        self.peoplePerceptionProxy.resetPopulation()
        self.peopleSubscriber = self.memoryService.subscriber("PeoplePerception/VisiblePeopleList")
        self.peopleSubscriber.signal.connect(self.onPeeps)
        print "Connected"
        self.peoplePerceptionService = self.session.service("ALPeoplePerception")
        self.peoplePerceptionService.subscribe("PeoplePerception")
        #time.sleep(30)

    def onPeeps(self, value):
        print "hey!"
        print value
        if len(value) > 0:
            for id in value:
                peepAt = self.memoryProxy.getData("PeoplePerception/Person/" + str(id) + "/PositionInWorldFrame")[0:2]
                print peepAt
                if self.testCoords(peepAt):
                    self.say("I'm waiting for you.")
                    self.navigationProxy.stopExploration()
                    self.moving = False
                else:
                    if self.moving == False:
                        self.say("I'm going into the lift")
                        self.moving = True
                        #coords = self.locations["inside door"]
                        #thread.start_new_thread(self.goHere,(coords[0],coords[1],coords[2]))
                        self.goHere(self.locations["lift back"])
                        self.moving = False


    def testCoords(self,p3):
        p1 = [-0.040594328194856644, 0.8543727397918701]
        p2 = [-0.5402392148971558, -1.4770621061325073]
        # p3 = [-1.5,0.3]

        xmin = min(p1[0],p2[0]) - 0.1
        ymin = min(p1[1],p2[1]) - 0.1
        xmax = max(p1[0],p2[0]) + 0.1
        ymax = max(p1[1],p2[1]) + 0.1


        if xmin <= p3[0] <= xmax and ymin <= p3[1] <= ymax:
            return True
        else:
            return False

    def load_dict(self):
        #loads a dictionary from the locations json file
        json_name = 'locations.json'

        with open(json_name) as json_data:
            self.locations = json.load(json_data)

        print("using locations file: " + json_name)

if __name__ == '__main__':
    pper = PeoplePerception(robotIP, PORT)
    pper.load_dict()
    pper.whosThere()

    #while loop keeps script alive for the threads to run. Super bad but
    #can change for the real thing.
    while True:
        pper.peoplePerceptionProxy.resetPopulation()
        time.sleep(5)
        pass
