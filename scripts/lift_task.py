#!/usr/bin/env python

from pepper_controller import PepperController
from pre_task import PreTask
import api_querier
import numpy


# pip install pillow
try:
    from PIL import Image
except ImportError:
    import Image

robotIP = "10.2.0.112" #Stevey


PORT = 9559

class LiftTask(PepperController):


	def prepClasses(self):
		#set up instances of classes from other files that we're going to need
		self.apiQuery = api_querier.api_querier()

	def getGoal(self):
		#Gets the goal floor from the data hub and returns it using alex's API
		shopList = self.apiQuery.get("Shop")

		### If there will only be a single goal - this option is better.
			# It will give you all the details about the object:

		# # Check how many shops are listed as a goal:
		# numGoals = 0
		# for shop in shopList:
		# 	if shop["goal"] == True:
		# 		numGoals = numGoals + 1
		#
		# # If there's only one goal, send the shop object:
		# if numGoals == 1:
	 	for shop in shopList:
	 		if shop["goal"]==True:
	 			return shop

		### If there are likely to be multiple goals, this option works:
			# It will return a dictionary of shop_descript(name) : shop_floor
		#try:
		#	goalList = {}
		#	#iterate through all shops in the returned msg
		#	for shop in shopList:
		#			# add any shops where goal is true to the dict
		#			if shop["goal"]==True:
		#				goalList[shop["description"]] = shop["floor"]

			# return goals:
		#	return goalList
		#except:
			# failed return -1
		#	return -1

	def startTask(self):
		#TODO A Request floor destination from DataHub (Alex Sleat)
		self.goalFloor = self.getGoal()
    	print self.goalFloor
    	# #print "Goal is " + g["description"] + " on floor " + str(g["floor"])
    	# liftTask.say("I'm visiting: ")
        #
    	# for key in self.goalFloor:
    	# 	s = str(key + " on floor "+ str(self.goalFloor[key]))
    	# 	liftTask.say(s)
        #
    	# if self.goalFloor==-1:
    	# 	print "Alex deserves more dessert today"

		#TODO B Decide where to go according to floor (Same floor or different floor)

		#TODO C If same floor go to goal and finish
		if self.goalFloor == 0:
			self.goHere(self.locations['finish'])
		else:
			#TODO D If different floor continue to next to TODOE
			#TODO E Approach to lift (Currently tested at the moment through threading**)
			self.goHere(self.locations['lift'])

			#TODO F Communicate that it has arrived at the waiting position
			self.say("I am waiting for the lift to arrive!")

			'''
				#Not sure it's necessary to post our location at this point, or, indeed, ever. (see API diagram for task)
				# d = qb.load_schema("RobotLocation") #Wait for Alex Sleat to confirm
				# qb.post("RobotLocation", d)
			'''



			'''
				Not planning to have interaction before we get to the lift, though it may be easy points if the lift section messes up
				#TODO G Engage with people if necessary
				#TODO Check for people around
                self.setVocabulary()
                self.speechRecognition()
					#TODO Also check for sounds that indicate willingness of interaction ("Hello", "Hey", "Excuse me" or voice very close to pepper)
					#TODO Detects gestures like waving
				#TODO Look at the closest person or origin of sounds and gestures
				#TODO Talk to the closest person
				#TODO Look at face
				#TODO GA Detect if the person wants to engage or not and act accordingly (If YES say name and communicate intention if NO just avoit/dodge)
					# TODO self.say("Hello, my name is pepper and I am going to floor" + str(FloorNumber))
					# OPTIONAL TODO person_comments = self.listen
			'''

			#Wait for all people to enter the lift
			#TODO how are we going to figure out if everyone's in the lift?
				#Wait until (Closest person distance (Known from cameras) == Lift distance (Known from map)) ?

			#Enter lift
			self.goHere(self.locations['lift entrance'])
			self.goHere(self.locations['lift riding']) # We assume pepper adapts trajectory to reduce distance
			# TODO Once pepper coordinates ensure it is inside the lift, Abort navigation.



	def InsideLift(self):
		#TODO 1 Locate itself in proper place
		#TODO 2 Face someone in the lift
        self.setVocabulary()
        self.speechRecognition()
		    #TODO 21 Check people around
		#TODO 2 Declare which floor the robot needs to go to
		    # self.say("Hello human, Could you help me by letting me know when we have reached floor number" + str(FloorNumber) + "?")
		    # person_intention = self.listen("Yes") # If YES thank if !YES repeat from TODO 2

		#TODO 3 Ask confirmation of action
		    # self.say("Thank you, human. You can call me Pepper")
		#TODO 4 Detect door opening
		    # TODO listen2door TOPIC????? Not a topic, we have to detect it on our own.
		#TODO 5 Ask someone which is the current floor to STAY or EXIT
		    #self.say("Excuse me. May I ask you if we are on floor number" + str(FloorNumber) +"?")
		    #person_answer = self.listen ("FloorNumber", "Yes")
		    #If True go to TODO_7 if False go to TODO_6
			#TODO 6 If STAY check if blocking entrance
				#TODO 8 If YES Exit, wait and re-enter
		            #self.goHere("Lift entrance coordinates")
		            #self.say("Please, someone help me keep the doors open. I need to go back in")
		            #self.goHere("Lift wall back coordinates") # Stop when inside the lift and enough far from door to closest
		            #self.goHere("Thank you all")
				#TODO 9 If NO go back to TODO4
			#TODO 7 If EXIT go out go to TODO10
			         #self.goHere("Lift entrance coordinates")

		#TODO 10 Not needed yet

	 def toEnd(self):
	 	self.say("This is my floor!")
         #TODO Wait for people to leave the lift
	
	 	self.say("I'm getting out now, thanks for your help!")
     	#Go to destination location
        
        #TODO need to fix the json stuff before this will work
	 	tread.start_new_thread(self.goHere,(self.locations['finish'],)  
	
	 	#TODO G Engage with people if necessary
	 	#TODO Check for people around
	 		#TODO Also check for sounds that indicate willingness of interaction ("Hello", "Hey", "Excuse me" or voice very close to pepper)
	 		#TODO Detects gestures like waving
	 	#TODO Look at the closest person or origin of sounds and gestures
	 	#TODO Talk to the closest person
	 	#TODO Look at face
	 	#TODO GA Detect if the person wants to engage or not and act accordingly (If YES say name and communicate intention if NO just avoit/dodge)
	 		# TODO self.say("Hello, my name is pepper and I am going to floor" + str(FloorNumber))
	 		# OPTIONAL TODO person_comments = self.listen
         #TODO c Acknowledge that the destination has been reached


    # def load_dict(self):
    #     #loads a dictionary from the locations json file
    #     json_name = 'locations.json'
	#
    #     with open(json_name) as json_data:
    #         self.locations = json.load(json_data)
	#
    #     print("using locations file: " + json_name)
	#
    # '''
    # def write_dict(self, updatedLocations):
    #     # todo: path as ros param
    #     json_name = rospy.get_param('locations_json')
    #     with open(json_file, "w") as JSonDictFile:
    #         json.dump(updatedLocations, json_file)
    # '''
if __name__ == '__main__':

	liftTask = LiftTask(robotIP, PORT)
	liftTask.prepClasses()
	# g = liftTask.getGoal()
	# print g
	# #print "Goal is " + g["description"] + " on floor " + str(g["floor"])
	# liftTask.say("I'm visiting: ")
    #
	# for key in g:
	# 	s = str(key + " on floor "+ str(g[key]))
	# 	liftTask.say(s)
    #
	# if g==-1:
	# 	print "Alex deserves more dessert today"

	liftTask.startTask()
	# liftTask.InsideLift()
	# liftTask.toEnd()
