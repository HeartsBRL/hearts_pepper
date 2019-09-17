#!/usr/bin/env python

from pepper_controller import PepperController
# from pre_task import PreTask
from api_querier import ApiQuerier
import numpy
import json
import time

# pip install pillow
try:
        from PIL import Image
except ImportError:
        import Image

robotIP = "westey.local" #Stevey


PORT = 9559

class LiftTask(PepperController):

    def prepClasses(self):
        #set up instances of classes from other files that we're going to need
        self.apiQuery = ApiQuerier()

    def getGoal(self):
        #Gets the goal floor from the data hub and returns it using alex's API
        shopList = self.apiQuery.get("Shop")

        ### If there will only be a single goal - this option is better.
            # It will give you all the details about the object:

        # # Check how many shops are listed as a goal:
        # numGoals = 0
        # for shop in shopList:
        #   if shop["goal"] == True:
        #        numGoals = numGoals + 1
        #
        # # If there's only one goal, send the shop object:
        # if numGoals == 1:
            # for shop in shopList:
            # 	if shop["goal"]==True:
            # 		return shop

        ### If there are likely to be multiple goals, this option works:
        	# It will return a dictionary of shop_descript(name) : shop_floor
        try:
            goalList = {}
            #iterate through all shops in the returned msg
            for shop in shopList:
                # add any shops where goal is true to the dict
                if shop["goal"]==True:
                    goalList[shop["description"]] = shop["floor"]

            # return goals:
            return goalList
        except:
            # failed return -1
            return -1

    def load_dict(self):
        #loads a dictionary from the locations json file
        json_name = 'locations.json'

        with open(json_name) as json_data:
            self.locations = json.load(json_data)

        print("using locations file: " + json_name)

    def sendInfo(self, schema, x, y, z, message=""):
        if schema!="RobotStatus" and schema!="RobotLocation":
            print 'The schema format is not correct. Nothing was sent Try: "RobotStatus" or "RobotLocation"'
            return -1
        elif schema=="RobotStatus" and message=="":
            print 'No message received. Nothing was sent. To send a "RobotStatus" schema you NEED to introduce a message'
            return -1
        else:
            try:
                ## Send object to server:
                print "Sending Robot Status rqst"
                # load the data schema for the item:
                # Example "RobotStatus" or "RobotLocation"
                t = str(datetime.datetime.now()).replace(" ", "T")
                t = t[:len(t)-3]+"Z"
                d = qb.load_schema(schema)
                if schema =="RobotStatus":
                    d["message"] = message
                d["@id"] = "hearts-pepper-" + t
                d["episode"] = "EPISODE4"
                d["team"] = "hearts"
                d["timestamp"] = t
                d["x"] = x
                d["y"] = y
                d["z"] = z
                qb.post(schema, d)
            except:
                # failed return -1
                return -1


    # def NewPerson_Callback(self):



    def startRecogPeople(self):
        # self.peoplePerceptionProxy.setFastModeEnabled(True)
        # print self.peoplePerceptionProxy.isMovementDetectionEnabled()
        # self.say("I am seeing you!")
        # self.memoryProxy.declareEvent("PeoplePerception/JustArrived")
        # self.memoryProxy.subscribeToEvent("PeoplePerception/JustArrived", const std::string& callbackModule, self.NewPerson_Callback)

        # Add target to track.
        targetName = "Face"
        faceWidth = 0.1
        self.trackerProxy.registerTarget(targetName, faceWidth)

        # Then, start tracker.
        self.trackerProxy.track(targetName)
        # self.memoryProxy.getEventHistory("PeoplePerception/JustArrived")
        print "ALTracker successfully started, now show your face to robot!"


    def stopRecogPeople(self):

        # Stop tracker.
        self.trackerProxy.stopTracker()
        self.trackerProxy.unregisterAllTargets()
        # self.motionProxy.rest()

        print "ALTracker stopped."

    def stuff(self):
        print "Use Ctrl+c to stop this script."
        try:
            while True:
                time.sleep(0.5)
                dark = self.memoryProxy.getData("DarknessDetection/DarknessValue")
                backlight = self.memoryProxy.getData("BacklightingDetection/BacklightingValue")

                # Exposition = self.cameraProxy.getParam("kCameraAutoExpositionID")
                # Gain = self.cameraProxy.getParam("kCameraAutoExpositionID")
                print dark
                print backlight
                # print Exposition
                # print Gain
        except KeyboardInterrupt:
            print "Interrupted by user"
            print "Stopping..."

if __name__ == '__main__':

    liftTask = LiftTask(robotIP, PORT)
    liftTask.prepClasses()
    liftTask.load_dict()
    # #TODO A Request floor destination from DataHub (Alex Sleat)
    # liftTask.g = liftTask.getGoal() # Name of the shop plus number as dictionary entry
    # if liftTask.g==-1:
    #     liftTask.say("Please, call my engineers. Something went wrong with the a p i querier")
    # else:
    #     liftTask.say("I'm visiting: ")
    #     for key in liftTask.g:
    #         s = str(key + " on floor "+ str(liftTask.g[key]))
    #         liftTask.goalFloor = str(liftTask.g[key]) # Just the number of the floor
    #         liftTask.shopName = str(key) # Just the number of the floor
    #         liftTask.say(s)
####People face tracking#####
    # liftTask.lifeProxy.setState("solitary")
    # liftTask.setVocabulary() # Set vocabulary now for subsequent speechRecognition activations
    # liftTask.say("\\vol=60\\I am speaking louder")
    # liftTask.say("\\vol=30\\I am speaking softer")
    liftTask.say("Good luck, Hearts team. You can do it!")
    liftTask.stuff()
    # liftTask.wakePepperUp()
    # liftTask.startRecogPeople()
    # liftTask.say("Detecting humans mode activated. Shoot to kill!")
    #
    # print "Use Ctrl+c to stop this script."
    # try:
    #     while True:
    #         time.sleep(1)
    #         print liftTask.memoryProxy.getData("DarknessDetection/DarknessValue")
    #         print liftTask.memoryProxy.getData("BacklightingDetection/BacklightingValue")
    # except KeyboardInterrupt:
    #     print "Interrupted by user"
    #     print "Stopping..."
    # liftTask.stopRecogPeople()
    # liftTask.goToSleep()

    ##### BACKLIGHTING Test#####
    # print "Use Ctrl+c to stop this script."
    # try:
    #     while True:
    #         time.sleep(0.5)
            # print liftTask.memoryProxy.getData("DarknessDetection/DarknessValue")
            # print liftTask.memoryProxy.getData("BacklightingDetection/BacklightingValue")
    # except KeyboardInterrupt:
    #     print "Interrupted by user"
    #     print "Stopping..."
