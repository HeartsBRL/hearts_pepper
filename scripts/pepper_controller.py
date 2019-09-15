#!/usr/bin/env python


import os
import json
import time

import qi

# pip install pillow
try:
    from PIL import Image
except ImportError:
    import Image
import numpy

from naoqi import ALProxy

#robotIP = "pepper.local"
robotIP = "westey.local" #Stevey
PORT = 9559

class PepperController(object):

    def __init__(self, ip, port):
        # Get the IP and port from the arguments
        self._robotIP = ip
        self._PORT = port
        # Start a session on the robot
        self.session = qi.Session()
        self.setup()

        self.old_recog = ""
        self.moving = False

    def ping(self):
        # Ping the robot
        response = os.system("ping -c 1 " + self._robotIP)
        # Check the response
        if response == 0:
            pingStatus = True
        else:
            pingStatus = False

        return pingStatus


    def setup(self):

        try:
            ## Try to connect to the robot at the given IP address
            self.session.connect("tcp://" + self._robotIP + ":" + str(self._PORT))

        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + self._robotIP + "\" on port " + str(self._PORT) +".\n"
              + "Please check your script arguments. Run with -h option for help.")

        try:
            ## ALL THE PROXIES
            self.tabletProxy = ALProxy("ALTabletService", self._robotIP, self._PORT)
            self.anSpeechProxy = ALProxy("ALAnimatedSpeech", self._robotIP, self._PORT)
            self.ttsProxy = ALProxy("ALTextToSpeech", self._robotIP, self._PORT)

            self.motionProxy  = ALProxy("ALMotion", self._robotIP, self._PORT)
            self.localizationProxy = ALProxy("ALLocalization", self._robotIP, self._PORT)
            self.memoryProxy = ALProxy("ALMemory", self._robotIP, self._PORT)
            self.navigationProxy = ALProxy("ALNavigation", self._robotIP, self._PORT)

            self.baProxy = ALProxy("ALBasicAwareness", self._robotIP, self._PORT)

            self.listeningProxy = ALProxy("ALListeningMovement", self._robotIP, self._PORT)
            self.lifeProxy = ALProxy("ALAutonomousLife", self._robotIP, self._PORT)
            self.dialogProxy = ALProxy("ALDialog", self._robotIP, self._PORT)
            self.system = ALProxy("ALSystem", self._robotIP, self._PORT)
            self.postureProxy = ALProxy("ALRobotPosture", self._robotIP, self._PORT)

            self.speechRecogProxy = ALProxy("ALSpeechRecognition", self._robotIP, self._PORT)
            self.engageProxy = ALProxy("ALEngagementZones", self._robotIP, self._PORT)
            self.peoplePerceptionProxy = ALProxy("ALPeoplePerception", self._robotIP, self._PORT)
            #self.waveDetectProxy = ALProxy("ALWavingDetection", self._robotIP, self._PORT)
            self.gazeProxy = ALProxy("ALGazeAnalysis", self._robotIP, self._PORT)
            self.faceDetectionProxy = ALProxy("ALFaceDetection", self._robotIP, self._PORT)
            self.soundLocalProxy = ALProxy("ALSoundLocalization", self._robotIP, self._PORT)
            self.soundDetectProxy = ALProxy("ALSoundDetection", self._robotIP, self._PORT)
            self.trackerProxy = ALProxy("ALTracker", self._robotIP, self._PORT)

            self.tabletProxy = ALProxy("ALTabletService", self._robotIP, self._PORT)
            self.tabletTimeoutLength = 60 #seconds
            self.tabletTimeout = time.time()
            self.tabletFlag = False

            self.memoryService = self.session.service("ALMemory")
            self.peoplePerceptionService = self.session.service("ALPeoplePerception")


            print("Connected to Pepper at " + self._robotIP + ":" + str(self._PORT))



        except Exception,e:
            print("Failed to connect to Pepper, is it on, and is the IP address correct?")
            print("IP : " + self._robotIP)
            print("PORT : " + str(self._PORT))
            print(e)

        ## Turn of auto-interaction features
        self.lifeProxy.setState("solitary")
        ## Set how close Pepper is allowed to get to obstacles
        self.motionProxy.setTangentialSecurityDistance(0.01)
        self.motionProxy.setOrthogonalSecurityDistance(0.05)
        self.postureProxy.goToPosture("Stand",0.6)
        self.peoplePerceptionService.subscribe("PeoplePerception")


    def say(self, words):

        print ("Saying: " + words)

        try:
            #Contextual animated say
            #self.anSpeechProxy.say(words)
            # Normal say
            self.ttsProxy.say(words)
        except Exception,e:
            print("Pepper TTS failed due to:")
            print(e)
        return

    def goHere(self,x,y,t):
        #simple function to call navigation. Can run this as a thread.

        #store intended coords as a tuple in case we need to resume this navigation command later
        self.going = (x,y,t)
        print("Going to " + str(self.going))
        ret = 1
        tries = 0
        while ret != 0 and tries < 10:
            ret = self.navigationProxy.navigateToInMap((x,y,t))
            tries += 1
        return ret

    def moveHere(self,x,y,t):
        #simple function to call navigation. Can run this as a thread.
        #store intended coords as a tuple in case we need to resume this navigation command later

        self.going = [x,y,t]
        print("Going to " + str(self.going))
        ret = False
        tries = 0
        self.current = self.motionProxy.getRobotPosition(True)
        #self.diff = self.current - self.going
        self.diff = [self.going[0]-self.current[0],self.going[1]-self.current[1],self.going[2]-self.current[2]]
        print("Moving by: " + str(self.diff))
        #while ret != True and tries < 5:
        ret = self.navgationProxy.navigateTo(*self.diff)
        #tries += 1
        #return ret

    def peopleInFront(self):
        zone1 = self.memoryProxy.getData("EngagementZones/PeopleInZone1")
        return zone1

    #### Methods for recognising words and locating sounds ###
    def setVocabulary(self):
        self.speechRecogProxy.pause(True)
        self.speechRecogProxy.removeAllContext()
        try:
            self.speechRecogProxy.setLanguage("English")
            self.speechRecogProxy.setVocabulary(["pepper", "yes", "we are here"],False)
        except:
            print("Vocabulary already set")
        self.speechRecogProxy.pause(False)

    def speechRecogThread(self):
        thread.start_new_thread(self.onWordRecognized,("words", 2))
        time.sleep(15)

    def speechRecognition(self):
        self.memoryProxy.insertData("WordRecognized", " ")
        self.speechRecogProxy.subscribe("attention")
        self.soundLocalProxy.subscribe("soundLocal")
        #self.speechRecogThread()
        print "Speech recognition engine started"
        self.onWordRecognized()

    def onWordRecognized(self):#, string, threadName):
        heard = False
        while heard == False:
            wordRecognized = self.memoryProxy.getData("WordRecognized")

            if(wordRecognized != self.old_recog):
                self.old_recog = wordRecognized

                print (wordRecognized)

            if wordRecognized[0] == "pepper":
                heard = True
                #self.trackSound()
                self.unsubscribe()

            if wordRecognized[0] == "yes":
                #self.trackSound()
                self.say("Thank you human")

            if wordRecognized[0] == "we are here":
                heard = True
                #self.trackSound()
                self.unsubscribe()
                self.say("Thank you, if anyone needs to get out of the lift please go before me")
                time.sleep(2)

    # def	trackSound(self):
        # targetName = "Sound"
        # param = [1, 0.1]
        # mode = "Move"

        # self.trackerProxy.registerTarget(targetName, param)
        # time.sleep(2)
        # activeTarget = self.trackerProxy.getActiveTarget()
        # print("target is: ", activeTarget)
        # self.trackerProxy.setMode(mode)
        # time.sleep(2)
        # activeMode = self.trackerProxy.getMode()
        # print("Mode is: ", activeMode)
        # self.trackerProxy.track(targetName)
        # time.sleep(0.5)
        # self.trackerProxy.stopTracker()
        # self.trackerProxy.unregisterAllTargets()

    def unsubscribe(self):
        self.speechRecogProxy.unsubscribe("attention")
        print "Speech recognition engine stopped"

        self.soundLocalProxy.unsubscribe("soundLocal")
        print "Sound localisation stopped"


if __name__ == '__main__':
    pepper = PepperController(robotIP, PORT)
    # while True:
    #     words = input("Enter a phrase! ")
    #     pepper.say(str(words))

    # while True:
    #     web = input("Enter a website ")
    #     pepper.display(web)
    #     input("Enter anything to hide website")
    #     pepper.stopDisplay()
