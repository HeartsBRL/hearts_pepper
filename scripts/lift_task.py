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

robotIP = "westey.local" #Westey

#PORT = 33579
PORT = 9559

class LiftTask(PepperController):

    def prepClasses(self):
        #set up instances of classes from other files that we're going to need
        self.apiQuery = ApiQuerier()

    def getGoal(self):
        #Gets the goal floor from the data hub and returns it using alex's API
        shopList = self.apiQuery.get("Shop")

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

    def startTask(self):

        self.moveHere(*self.locations['start'])
        if self.goalFloor == 0:
            self.say("I'm already on this floor, I'm going to the finish")
            #self.extraInteraction()
            self.moveHere(*self.locations['finish'])
            print "Going to the final destination"
        else:
            
            self.say("I will need to use the lift to get there.")
            #self.extraInteraction()
           # self.moveHere(*self.locations['near lift'])
            self.moveHere(*self.locations['zone1'])
            self.moveHere(*self.locations['zone2'])
            self.moveHere(*self.locations['zone3'])
            #self.extraInteraction()?
            self.moveHere(*self.locations['near lift 2'])
            self.lifeProxy.setState("solitary")
            self.say("Hi everyone, I am Pepper. I'll wait, please go ahead of me.")
            #TODO Approach to lift, define new location/people perception

            freedom = 0
            while freedom < 50:
                if len(self.peopleAround()) > 0:
                    #self.say("Get in the lift!") #MAKE SURE TO COMMENT
                    freedom = 0
                else:
                    freedom += 1

            self.say("I'm going to the lift now.")
            self.lifeProxy.setState("safeguard")
            self.postureProxy.goToPosture("Stand",0.6)
            self.moveHere(*self.locations['outside door'])
            self.moveHere(*self.locations['inside door'])
            self.say("Excuse me please. I would like to stand at the back of the lift")

            time.sleep(2)
            self.moveHere(*self.locations['lift back'])
            self.motionProxy.moveTo(0,0,3.14159)



         #TODO IMPROVEMENTS
            # Find appropriate location in lift
           
            #Post our location at various points
            # self.sendInfo("RobotStatus",0,0,0, "Waiting for elevator")
            #self.sendInfo("RobotStatus",self.locations['lift back'][0],self.locations['lift back'][1],self.locations['lift back'][2], "Waiting for elevator")
            # self.sendInfo("RobotLocation",0,0,0)
            #self.sendInfo("RobotLocation",self.locations['lift back'][0],self.locations['lift back'][1],self.locations['lift back'][2])


    def postLocation():
        
    



    def InsideLift(self):
        self.say("Thank you. Could you please press floor " + str(self.goalFloor) + "?")
        self.doorOpen = False
        self.rightFloor = False
        self.senseTouch()

        while self.rightFloor == False:

            self.expectingTouch = False

            while self.doorOpen == False:
                self.findBlobs()
            
            self.doorOpen = False
            self.say("Is this floor " + str(self.goalFloor) + "? If so, please touch the top of my head.")
            self.expectingTouch = True
            time.sleep(10)
            
        #TODO Improvements:
            # Recognise that people say no when it's not the right floor
            # Face people in lift when talking    
            # Get confirmation of button press
            # Move if we're in the way

#####################################################################################################
    def toEnd(self):
        self.say("This is my floor!")
        #self.lifeProxy.setState("solitary")
        self.say("I'm getting out now, thank you for your help! Have a good day!")
        self.moveHere(*self.locations['inside door'])
        self.moveHere(*self.locations['outside door'])
        #self.extraInteraction()?
        self.moveHere(*self.locations['pre finish'])
        self.moveHere(*self.locations['finish'])
        self.moveHere(*self.locations['extra finish'])

        #TODO Improvements
            # Wait for people to leave before we move



    def extraInteraction(self):

        dests = ['zone1','zone2','zone3']
        for dest in dests:            
            x,y,t = self.locations[dest]
            self.moveHere(x,y,t,True)
            self.speechRecognition()
            while self.navigationProxy.isRunning(self.threadID) and self.heard == False:
                pass
            if self.heard == True: 
                break

        self.navigationProxy.stopExploration()
        self.lifeProxy.setState("solitary")
        peeps = []
        breakCondition = 0
        while len(peeps) == 0 and breakCondition < 50:
            peeps = self.peopleAround(3)
            breakCondition += 1

        for person in peeps:
            if self.memoryProxy.getData("PeoplePerception/Person/" + person + "/IsLookingAtRobot") == True:
                self.lookingAtMe = person
                self.trackerProxy.registerTarget("Person", person)
                self.trackerProxy.track("Person")

        while len(peeps) == 0 and breakCondition < 50:
            peeps = self.peopleAround(1)
            breakCondition += 1

        self.say("Hi human, I'm sorry but I already have a task that I need to complete. I hope you can find someone else to help you!")

        self.trackerProxy.stopTracker()
        self.trackerProxy.unregisterAllTargets()

        self.lifeProxy.setState("safeguard")
        self.postureProxy.goToPosture("Stand",0.6)
        self.moveHere(*self.locations['zone3'])
        #TODO Improvements
            # Look for person that's walking towards pepper	    





if __name__ == '__main__':

	#DEFINE CLASS#
    liftTask = LiftTask(robotIP, PORT)

	#SETUP- PREPARE LIST OF LOCATIONS FROM DATAHUB AND SET VOCABULARY#
    liftTask.prepClasses()
    liftTask.load_dict()
    #Request floor destination from DataHub (Alex Sleat)
    liftTask.g = liftTask.getGoal() # Name of the shop plus number as dictionary entry
    if liftTask.g==-1:
        liftTask.say("Please, call my engineers. Something went wrong with the a p i querier")
    else:
        liftTask.say("I'm visiting: ")
        for key in liftTask.g:
            s = str(key + " on floor "+ str(liftTask.g[key]))
            liftTask.goalFloor = str(liftTask.g[key]) # Just the number of the floor
            liftTask.shopName = str(key) # Just the number of the floor
            liftTask.say(s)
    liftTask.setVocabulary() # Set vocabulary now for subsequent speechRecognition activations

	#GO TO LIFT AND WAIT FOR PEOPLE TO ENTER THE LIFT BEFORE WE DO#
    liftTask.startTask()

	#ONCE INSIDE LIFT ASK FOR ASSISTANCE GETTING TO CORRECT FLOOR AND LISTEN FOR RESPONSE#
    liftTask.InsideLift()

	#LEAVE LIFT AND GO TO FINISH, INTERACTING WITH PEOPLE ON THE WAY#
    liftTask.toEnd()
