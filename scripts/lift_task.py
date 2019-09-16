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

robotIP = "stevey.local" #Stevey


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

    def startTask(self):

        #self.goHere(*self.locations['start'])
        if self.goalFloor == 0:
            self.say("I'm already on this floor, I'm going to the finish")
            self.goHere(*self.locations['finish'])
            print "Going to the final destination"
        else:
            self.say("I will need to use the lift to get there.")
            #self.goHere(*self.locations['near lift'])
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
            #self.goHere(*self.locations['outside door'])
            #self.goHere(*self.locations['inside door'])
            self.say("Excuse me please. I would like to stand at the back of the lift")

            time.sleep(2)
            #self.goHere(*self.locations['lift back'])
            #self.motionProxy.moveTo(0,0,3.14159)



         #OPTIONAL IMPROVEMENTS#

            #TODO find location in lift
            #go to place in lift
            # self.goHere(*self.locations['lift inside'])
            #self.goHere(*self.locations['lift back']) # We assume pepper adapts trajectory to reduce distance


         #TODO F Communicate that it has arrived at the waiting position - probably dont need
            # self.sendInfo("RobotStatus",0,0,0, "Waiting for elevator")
            #self.sendInfo("RobotStatus",self.locations['lift back'][0],self.locations['lift back'][1],self.locations['lift back'][2], "Waiting for elevator")
            # self.sendInfo("RobotLocation",0,0,0)
            #self.sendInfo("RobotLocation",self.locations['lift back'][0],self.locations['lift back'][1],self.locations['lift back'][2])



        #
        #		 #Wait for all people to enter the lift
        #		 #TODO how are we going to figure out if everyone's in the lift?
        #			 #Wait until (Closest person distance (Known from cameras) == Lift distance (Known from map)) ?
        #
        #		 #Enter lift
        #		 # TODO Once pepper coordinates ensure it is inside the lift, Abort navigation.
        #
        #
        #



    def InsideLift(self):
        self.say("Could you touch my head when we have reached floor number " + str(self.goalFloor) + "please?")
        self.expectingTouch = True
        self.senseTouch()
        while self.expectingTouch == True:
            pass



    #	 #TODO 2 Face someone in the lift
    			# self.speechRecognition()
    #			 #TODO 21 Check people around

    #			 # person_intention = self.listen("Yes") # If YES thank if !YES repeat from TODO 2
    	#
    #	 #TODO 3 Ask confirmation of action - if yes say thanks
        #self.say("Thank you human.")
    #	 #TODO 4 Detect door opening
    #			 # TODO listen2door TOPIC????? Not a topic, we have to detect it on our own.
	# Ask humans to say when we're at the floor
	#When at the floor go toEnd

    #	 #TODO 5 are we in the way, if yes, move
        #self.say("Excuse me. May I ask you if we are on floor number " + str(self.goalFloor) +"?")
    #			 #person_answer = self.listen ("FloorNumber", "Yes")
    #			 #If True go to TODO_7 if False go to TODO_6
    #		 #TODO 6 If STAY check if blocking entrance
    #			 #TODO 8 If YES Exit, wait and re-enter
    				# self.goHere("Lift entrance coordinates")
    				# self.say("Please, someone help me keep the doors open. I need to go back in")
    				# self.goHere("Lift wall back coordinates") # Stop when inside the lift and enough far from door to closest
    				# self.goHere("Thank you all")
    #			 #TODO 9 If NO go back to TODO4
    #		 #TODO 7 If EXIT go out go to TODO10
    				# self.goHere("Lift entrance coordinates")

#####################################################################################################
    def toEnd(self):
        #self.say("This is my floor!")
    	#		 #TODO Wait for people to leave the lift
    #
        #self.lifeProxy.setState("solitary")
        self.say("I'm getting out now, thank you for your help! Have a good day!")
    	#	 #Go to destination location
        self.goHere(*self.locations['inside door'])
        self.goHere(*self.locations['outside door'])
		self.extraInteraction()
        self.goHere(*self.locations['finish'])





    def extraInteraction(self):

        self.goHere(*self.locations['finish'],True)
        self.SpeechRecognition()
        self.navigationProxy.stopExploration()
        self.lifeProxy.setState("solitary")
        peeps = self.peopleAround(3)

        for person in peeps:
            if self.memoryProxy.getData("PeoplePerception/Person/" + person + "/IsLookingAtRobot") == True:
                self.lookingAtMe = person
                self.trackerProxy.registerTarget("Person", person)
                self.trackerProxy.track("Person")

        self.say("Hi human, I'm sorry but I already have a task that I need to complete. I hope you can find someone else to help you!")

        self.trackerProxy.stopTracker()
        self.trackerProxy.unregisterAllTargets()

        self.lifeProxy.setState("safeguard")
        self.postureProxy.goToPosture("Stand",0.6)

	        #		 '''
        #			 Not planning to have interaction before we get to the lift, though it may be easy points if the lift sections messes up
        #			 #TODO G Engage with people if necessary
        #			 #TODO Check for people around
        # self.speechRecognition()
        #				 #TODO Also check for sounds that indicate willingness of interaction ("Hello", "Hey", "Excuse me" or voice very close to pepper)
        #				 #TODO Detects gestures like waving
        #			 #TODO Look at the closest person or origin of sounds and gestures
        #			 #TODO Talk to the closest person
        #			 #TODO Look at face
        #			 #TODO GA Detect if the person wants to engage or not and act accordingly (If YES say name and communicate intention if NO just avoit/dodge)
        #    self.say("Hello, my name is pepper and I am going to floor " + self.goalFloor)
        #				 # OPTIONAL TODO person_comments = self.listen

		    #	 #TODO G Engage with people if necessary
    #	 #TODO Check for people around
    #		 #TODO Also check for sounds that indicate willingness of interaction ("Hello", "Hey", "Excuse me" or voice very close to pepper)
    #		 #TODO Detects gestures like waving
    #	 #TODO Look at the closest person or origin of sounds and gestures
    #	 #TODO Talk to the closest person
    #	 #TODO Look at face
    #	 #TODO GA Detect if the person wants to engage or not and act accordingly (If YES say name and communicate intention if NO just avoit/dodge)
    #		 # TODO self.say("Hello, my name is pepper and I am going to floor" + str(FloorNumber))
    #		 # OPTIONAL TODO person_comments = self.listen
    	#		 #TODO c Acknowledge that the destination has been reached

        #		 '''

        pass



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
    #liftTask.setVocabulary() # Set vocabulary now for subsequent speechRecognition activations

	#GO TO LIFT AND WAIT FOR PEOPLE TO ENTER THE LIFT BEFORE WE DO#
    liftTask.startTask()

	#ONCE INSIDE LIFT ASK FOR ASSISTANCE GETTING TO CORRECT FLOOR AND LISTEN FOR RESPONSE#
    liftTask.InsideLift()

	#LEAVE LIFT AND GO TO FINISH, INTERACTING WITH PEOPLE ON THE WAY#
    liftTask.toEnd()
