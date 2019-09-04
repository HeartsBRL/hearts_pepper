#!/usr/bin/env python

from pepper_controller import PepperController
from pre_task import PreTask
import api_querier
import numpy
from api_querier import ApiQuerier


# pip install pillow
try:
    from PIL import Image
except ImportError:
    import Image

robotIP = "10.2.0.118" #Stevey


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
			return {}

if __name__ == '__main__':

    liftTask = LiftTask(robotIP, PORT)
    liftTask.prepClasses()
    g = liftTask.getGoal()
    print g
    #print "Goal is " + g["description"] + " on floor " + str(g["floor"])
    liftTask.say("I could murder a cheese burger please")
    liftTask.say("I'm visiting: ")

    for key in g:
        s = str(key + " on floor "+ str(g[key]))
        liftTask.say(s)

    if g==-1:
        print "Alex deserves more dessert today"
