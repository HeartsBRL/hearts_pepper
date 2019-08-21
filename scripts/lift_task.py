#!/usr/bin/env python

from pepper_controller import PepperController

import numpy
import Image

robotIP = "10.2.0.114" #Stevey
PORT = 9559

class LiftTask(PepperController):

    def toStart(self):
    	#TODOA Request floor destination to DataHub
    	#TODOB Decide if where to go according to floor (Same floor or different floor)
    		#TODOC If same floor go to goal and finish
    		self.navigationProxy.navigateToInMap((0,-1,-1))
    		#TODOD If different floor continue to next to TODOE
    	#TODOE Approach to lift
    	self.navigationProxy.navigateToInMap((0,-1,0))
    	#TODOF Communicate that it has arrived at the waiting position
    	#TODOG Engage with people if necessary
    		#TODOGA Detect if the person wants to engage or not and act accordingly (If YES say name and communicate intention)
    	#TODOH Wait for all people to enter the lift
    	#TODOI Enter lift
        self.navigationProxy.navigateToInMap((0,-1,1))

    def InsideLift(self):
    	#TODO1 Locate itself in proper place
    	#TODO2 Face someone in the lift
    	#TODO2 Declare which floor the robot needs to go to
    	#TODO3Ask confirmation of action
    	#TODO4 Detect door opening
    	#TODO5 Ask someone which is the current floor to STAY or EXIT
    		#TODO6 If STAY check if blocking entrance
    			#TODO8 If YES Exit, wait and re-enter
    			#TODO9 If NO go back to TODO4
    		#TODO7 If EXIT go out go to TODO10
			self.navigationProxy.navigateToInMap((0,0,0))  
		#TODO10 

         
    def toEnd(self):
    	#TODOa Go to destination location
    	self.navigationProxy.navigateToInMap((0,1,0))
    	#TODOb Engage with people if necessary
        	#TODOba Detect if the person wants to engage or not and act accordingly (If YES say name and communicate intention)
        #TODOc Acknowledge that the destination has been reached


if __name__ == '__main__':
    liftTask = LiftTask(robotIP, PORT)
    liftTask.toStart()
    liftTask.InsideLift()
    liftTask.toEnd()
