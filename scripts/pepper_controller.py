#!/usr/bin/env python


import os
import json
import time
import thread
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
            self.engagementProxy = ALProxy("ALEngagementZones", self._robotIP, self._PORT)
            self.peoplePerceptionProxy = ALProxy("ALPeoplePerception", self._robotIP, self._PORT)
            #self.waveDetectProxy = ALProxy("ALWavingDetection", self._robotIP, self._PORT)
            self.gazeProxy = ALProxy("ALGazeAnalysis", self._robotIP, self._PORT)
            self.faceDetectionProxy = ALProxy("ALFaceDetection", self._robotIP, self._PORT)
            self.soundLocalProxy = ALProxy("ALSoundLocalization", self._robotIP, self._PORT)
            self.soundDetectProxy = ALProxy("ALSoundDetection", self._robotIP, self._PORT)
            self.trackerProxy = ALProxy("ALTracker", self._robotIP, self._PORT)
            # self.cameraProxy = ALProxy("ALVideoDevice", self._robotIP, self._PORT)
            self.darknessProxy = ALProxy("ALDarknessDetection", self._robotIP, self._PORT)
            self.backLightningProxy = ALProxy("ALBacklightingDetection", self._robotIP, self._PORT)
            self.colourProxy = ALProxy("ALColorBlobDetection", self._robotIP, self._PORT)
            self.tabletProxy = ALProxy("ALTabletService", self._robotIP, self._PORT)
            self.tabletTimeoutLength = 60 #seconds
            self.tabletTimeout = time.time()
            self.tabletFlag = False

<<<<<<< HEAD
            self.memoryService = self.session.service("ALMemory")
            self.darknessService = self.session.service("ALDarknessDetection")
            self.backLightingService = self.session.service("ALBacklightingDetection")
=======
            self.memoryService = self.session.service("ALMemory")            
>>>>>>> 68b3e58b00f406f53f4b896dc2fa6ae0b89f6684
            self.peoplePerceptionService = self.session.service("ALPeoplePerception")
            self.darknessService = self.session.service("ALDarknessDetection")
            self.touchService = self.session.service("ALTouch")

            print("Connected to Pepper at " + self._robotIP + ":" + str(self._PORT))



        except Exception,e:
            print("Failed to connect to Pepper, is it on, and is the IP address correct?")
            print("IP : " + self._robotIP)
            print("PORT : " + str(self._PORT))
            print(e)

        ## Turn of auto-interaction features
        self.lifeProxy.setState("safeguard")
        ## Set how close Pepper is allowed to get to obstacles
        self.motionProxy.setTangentialSecurityDistance(0.01)
        self.motionProxy.setOrthogonalSecurityDistance(0.05)
        self.engagementProxy.setFirstLimitDistance(2.0)
        self.engagementProxy.setLimitAngle(180.0)
        self.postureProxy.goToPosture("Stand",0.6)
        self.peoplePerceptionService.subscribe("PeoplePerception")
<<<<<<< HEAD
        self.darknessService.subscribe("DarknessDetection")
        self.backLightingService.subscribe("BacklightningDetection")
=======
        self.darknessService.subscribe("Darkness")
>>>>>>> 68b3e58b00f406f53f4b896dc2fa6ae0b89f6684


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

    def senseColour(self):
        self.colourProxy.setColor(255,255,255,30)
        self.colourProxy.setObjectProperties(1,1)

    def findBlobs(self):
        blobsList = self.memoryProxy.getData("Segmentation3D/BlobsList")[1]
        for blob in blobsList:
            if blob[2] > 2:
                self.doorOpen = True



    def goHere(self,x,y,t, parallel=False):
        #simple function to call navigation. Can run this as a thread.
        #store intended coords as a tuple in case we need to resume this navigation command later

        self.going = (x,y,t)
        print("Going to " + str(self.going))
        ret = 1
        tries = 0
        if parallel == False:
            while ret != 0 and tries < 10:
                ret = self.navigationProxy.navigateToInMap((x,y,t))
                tries += 1
        else:
            ret = self.navigationProxy.post.navigateToInMap((x,y,t))
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

    def peopleAround(self, range=1):
        peeps = self.memoryProxy.getData("EngagementZones/PeopleInZone1")
        if range > 1:
            zone2 = self.memoryProxy.getData("EngagementZones/PeopleInZone2")
            for person in zone2:
                zone1.append(person)
        if range > 2:
            zone3 = self.memoryProxy.getData("EngagementZones/PeopleInZone3")
            for person in zone2:
                zone1.append(person)

        return peeps

        ###STOP robot movement
        # self.navigationProxy.stopExploration() #Stops pepper navigating

#### Methods for recognising words and locating sounds ###
    def setVocabulary(self):
        self.speechRecogProxy.pause(True)
        self.speechRecogProxy.removeAllContext()
        try:
            self.speechRecogProxy.setLanguage("English")
            self.speechRecogProxy.setVocabulary(["pepper", "yes"],False)
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
                self.trackSound()

            #if "pepper" in wordRecognized:

            #self.ttsProxy.say("I heard you")
                self.unsubscribe()

    def	trackSound(self):
        targetName = "Sound"
        param = [1, 0.1]
        mode = "Move"

        self.trackerProxy.registerTarget(targetName, param)
        time.sleep(2)
        activeTarget = self.trackerProxy.getActiveTarget()
        print("target is: ", activeTarget)
        self.trackerProxy.setMode(mode)
        time.sleep(2)
        activeMode = self.trackerProxy.getMode()
        print("Mode is: ", activeMode)
        self.trackerProxy.track(targetName)
        time.sleep(0.5)
        self.trackerProxy.stopTracker()
        self.trackerProxy.unregisterAllTargets()

    def senseTouch(self):
        self.frontTouchSubscriber = self.memoryService.subscriber("FrontTactilTouched")
        self.midTouchSubscriber = self.memoryService.subscriber("MiddleTactilTouched")
        self.backTouchSubscriber = self.memoryService.subscriber("RearTactilTouched")
        self.frontTouchSubscriber.signal.connect(self.reactToTouch)
        self.midTouchSubscriber.signal.connect(self.reactToTouch)
        self.backTouchSubscriber.signal.connect(self.reactToTouch)
        print "Connected"
        #self.touchService.subscribe("Touch")

    def reactToTouch(self, val):
        print val
        if self.expectingTouch == True and val == 1:
            self.expectingTouch = False
            time.sleep(1)

## Face/People Tracking#####

    def startRecogPeople(self):

        # Add target to track.
        targetName = "Face"
        faceWidth = 0.1
        self.trackerProxy.registerTarget(targetName, faceWidth)
        # Then, start tracker.
        self.trackerProxy.track(targetName)
        print "ALTracker successfully started, now show your face to robot!"


    def stopRecogPeople(self):

        # Stop tracker.
        self.trackerProxy.stopTracker()
        self.trackerProxy.unregisterAllTargets()
        print "ALTracker stopped."

###Miscellaneous###

    def unsubscribe(self):
        self.speechRecogProxy.unsubscribe("attention")
        print "Speech recognition engine stopped"

        self.soundLocalProxy.unsubscribe("soundLocal")
        print "Sound localisation stopped"

    def goToSleep(self):
        self.motionProxy.rest()
    def wakePepperUp(self):
        self.motionProxy.wakeUp()


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
