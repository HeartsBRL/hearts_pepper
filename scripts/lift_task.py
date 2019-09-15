	#!/usr/bin/env python

from pepper_controller import PepperController
# from pre_task import PreTask
from api_querier import ApiQuerier
import numpy
import json


# pip install pillow
try:
        from PIL import Image
except ImportError:
        import Image

robotIP = "10.2.0.111" #Stevey


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

        #TODO B Decide where to go according to floor (Same floor or different floor)
        self.goHere(*self.locations['start'])
        #TODO C If same floor go to goal and finish
        if self.goalFloor == 0:
            self.say("Enrouting to the final destination")
            self.goHere(*self.locations['finish'])
            print "Going to the final destination" #UNCOMMENT
        else:
        #TODO D If different floor continue to next to TODOE
        #TODO E Approach to lift (Currently tested at the moment through threading**)
            self.say("Enrouting to the entrance of the lift")
            self.goHere(*self.locations['outside door']) #UNCOMMENT
            print "Going to the back of the lift"

        #		 #TODO F Communicate that it has arrived at the waiting position
            self.say("I am waiting for the elevator to arrive!")
            # self.sendInfo("RobotStatus",0,0,0, "Waiting for elevator")
            self.sendInfo("RobotStatus",self.locations['lift back'][0],self.locations['lift back'][1],self.locations['lift back'][2], "Waiting for elevator")
            # self.sendInfo("RobotLocation",0,0,0)
            self.sendInfo("RobotLocation",self.locations['lift back'][0],self.locations['lift back'][1],self.locations['lift back'][2])

        #
        #		 '''
        #			 #Not sure it's necessary to post our location at this point, or, indeed, ever. (see API diagram for task)
        #			 # d = qb.load_schema("RobotLocation") #Wait for Alex Sleat to confirm
        #			 # qb.post("RobotLocation", d)
        #		 '''
        #
        #
        #
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
            self.say("Hello, my name is pepper and I am going to floor " + self.goalFloor)
        #				 # OPTIONAL TODO person_comments = self.listen
        #		 '''
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


            self.goHere(*self.locations['inside door'])
            self.say("Enrouting to the inside of the lift")
            # self.goHere(*self.locations['lift inside'])
            self.goHere(*self.locations['lift back']) # We assume pepper adapts trajectory to reduce distance

    def InsideLift(self):
        # self.setVocabulary()
        self.speechRecognition()
    #	 #TODO 1 Locate itself in proper place
    #	 #TODO 2 Face someone in the lift
    			# self.speechRecognition()
    #			 #TODO 21 Check people around
    #	 #TODO 2 Declare which floor the robot needs to go to
        self.say("Hello human, Could you help me by letting me know when we have reached floor number " + str(self.goalFloor) + "?")
    #			 # person_intention = self.listen("Yes") # If YES thank if !YES repeat from TODO 2
    	#
    #	 #TODO 3 Ask confirmation of action
        self.say("Thank you human. You can call me Pepper")
    #	 #TODO 4 Detect door opening
    #			 # TODO listen2door TOPIC????? Not a topic, we have to detect it on our own.
    #	 #TODO 5 Ask someone which is the current floor to STAY or EXIT
        self.say("Excuse me. May I ask you if we are on floor number " + str(self.goalFloor) +"?")
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
    	#
    #	 #TODO 10 Not needed yet
#####################################################################################################
    def toEnd(self):
        self.say("This is my floor!")
    	#		 #TODO Wait for people to leave the lift
    #
        self.say("I'm getting out now, thank all of you for your help! Have a good day!")
    	#	 #Go to destination location
        self.goHere(*self.locations['inside door'])
        self.goHere(*self.locations['outside door'])
        self.goHere(*self.locations['finish'])
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
    liftTask.toEnd()
