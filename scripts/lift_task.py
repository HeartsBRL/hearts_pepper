#!/usr/bin/env python

from pepper_controller import PepperController
from pre_task import PreTask
from api_querier import api_querier
import numpy
import Image

robotIP = "10.2.0.114" #Stevey
PORT = 9559

#class LiftTask(PepperController):
class LiftTask(Pretask, api_querier):


    def toStart(self):
    	#TODO A Request floor destination to DataHub
            qb = api_querier("master")
            #qb.get("RobotStatus")
            d = qb.load_schema("RobotLocation")
            qb.post("RobotLocation", d)

    	#TODO B Decide if where to go according to floor (Same floor or different floor)


    		#TODO C If same floor go to goal and finish
    		      self.goHere("Finish coordinates")
    		#TODO D If different floor continue to next to TODOE
    	#TODO E Approach to lift
    	   self.goHere("Lift coordinates")
           #TODO While robot is moving check if obstacles are met and dodge if posible or stop if goal reached or people blocking way.

    	#TODO F Communicate that it has arrived at the waiting position
            self.say("I am waiting for the elevator to arrive!")
            d = qb.load_schema("RobotLocation")
            qb.post("RobotLocation", d)
    	#TODO G Engage with people if necessary
            #TODO Check for people around
                #TODO Also check for sounds that indicate willingness of interaction ("Hello", "Hey", "Excuse me" or voice very close to pepper)
            #TODO Look at the closest person
            #TODO Talk to the closest person
            #TODO Look at face
    		#TODO GA Detect if the person wants to engage or not and act accordingly (If YES say name and communicate intention if NO just avoit/dodge)
                # TODO self.say("Hello, my name is pepper and I am going to floor" + str(FloorNumber))
                # OPTIONAL TODO person_comments = self.listen
        #TODO H Wait for all people to enter the lift
            #TODO Wait until (Closest person distance (Known from cameras) == Lift distance (Known from map))
        #TODO I Enter lift
        self.goHere("Lift Entrance coordinates")
        self.goHere("Lift back wall coordinates") # We assume pepper adapts trajectory to reduce distance
        # TODO Once pepper coordinates ensure it is inside the lift, Abort navigation.

    def InsideLift(self):
    	#TODO 1 Locate itself in proper place
    	#TODO 2 Face someone in the lift
            #TODO 21 Check people around
    	#TODO 2 Declare which floor the robot needs to go to
            # self.say("Hello human, Could you help me by letting me know when we have reached floor number" + str(FloorNumber) + "?")
            # person_intention = self.listen("Yes") # If YES thank if !YES repeat from TODO 2

    	#TODO 3 Ask confirmation of action
            # self.say("Thank you, human. You can call me Pepper")
    	#TODO 4 Detect door opening
            # TODO listen2door TOPIC?????
    	#TODO 5 Ask someone which is the current floor to STAY or EXIT
            #self.say("Excuse me. May I ask you if we are on floor number" + str(FloorNumber) +"?")
            #person_answer = self.listen ("FloorNumber")
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
    	#TODO a Go to destination location
    	#self.goHere("Finish coordinates")

        #### Already done on toStart method (Copy and parte here from there if needed)
    	#TODO b Engage with people if necessary
        	#TODO ba Detect if the person wants to engage or not and act accordingly (If YES say name and communicate intention)
        #TODO c Acknowledge that the destination has been reached


    def load_dict(self):
        
        json_name = 'locations.json'

        with open(json_name) as json_data:
            self.dict = json.load(json_data)

        print("using locations file: " + json_name)
        print(self.dict)

    '''
    def write_dict(self, updatedLocations):
        # todo: path as ros param
        json_name = rospy.get_param('locations_json')
        with open(json_file, "w") as JSonDictFile:
            json.dump(updatedLocations, json_file)
    '''

if __name__ == '__main__':
    liftTask = LiftTask(robotIP, PORT)
    liftTask.toStart()
    liftTask.InsideLift()
    liftTask.toEnd()
