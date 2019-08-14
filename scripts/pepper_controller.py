#!/usr/bin/env python


import os
import json
import time


import qi
import Image
import numpy

from naoqi import ALProxy

#robotIP = "pepper.local"
robotIP = "10.2.0.112" #Stevey
PORT = 9559

class PepperController(object):
    
    def __init__(self, ip, port):
        # Get the IP and port from the arguments 
        self._robotIP = ip
        self._PORT = port
        # Start a session on the robot
        self.session = qi.Session()
        self.setup()

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
               "Please check your script arguments. Run with -h option for help.")

        try:
            ## ALL THE PROXIES            
            self.tabletProxy = ALProxy("ALTabletService", self._robotIP, self._PORT)
            self.anSpeechProxy = ALProxy("ALAnimatedSpeech", self._robotIP, self._PORT)
            self.ttsProxy = ALProxy("ALTextToSpeech", self._robotIP, self._PORT)

            self.motionProxy  = ALProxy("ALMotion", self._robotIP, self._PORT)
            self.localizationProxy = ALProxy("ALLocalization", self._robotIP, self._PORT)

            self.navigationProxy = ALProxy("ALNavigation", self._robotIP, self._PORT)

            self.baProxy = ALProxy("ALBasicAwareness", self._robotIP, self._PORT)

            self.listeningProxy = ALProxy("ALListeningMovement", self._robotIP, self._PORT)
            self.lifeProxy = ALProxy("ALAutonomousLife", self._robotIP, self._PORT)
            self.dialogProxy = ALProxy("ALDialog", self._robotIP, self._PORT)
            self.system = ALProxy("ALSystem", self._robotIP, self._PORT)
            self.speechRecogProxy = ALProxy("ALSpeechRecognition", self._robotIP, self._PORT)

            self.faceDetectionProxy = ALProxy("ALFaceDetection", self._robotIP, self._PORT)
            self.memoryProxy = ALProxy("ALMemory", self._robotIP, self._PORT)
            self.trackerProxy = ALProxy("ALTracker", self._robotIP, self._PORT)
            self.motionProxy = ALProxy("ALMotion", self._robotIP, self._PORT)

            self.tabletProxy = ALProxy("ALTabletService", self._robotIP, self._PORT)
            self.tabletTimeoutLength = 60 #seconds
            self.tabletTimeout = time.time()
            self.tabletFlag = False

            print("Connected to Pepper at " + self._robotIP + ":" + str(self._PORT))

        except Exception,e:
            print("Failed to connect to Pepper, is it on, and is the IP address correct?")
            print("IP : " + self._robotIP)
            print("PORT : " + str(self._PORT))
            print(e)

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

    def display(self, filename):

        #@TODO add videos
        print ("Displaying: " + filename)
        self.tabletTimeout = time.time()
        try:
            video_ext = ["mp4"]
            img_ext = ["jpg", "jpeg", "png", "gif"]
            if(filename.endswith(tuple(img_ext))):
                r = self.tabletProxy.showImage(filename)
                self.tabletFlag = "image"
            elif(filename.endswith(tuple(video_ext))):
                r = self.tabletProxy.playVideo(filename)
                self.tabletFlag = "video"
            else:
                r = self.tabletProxy.showWebview(filename)
                self.tabletFlag = "webview"

            print(self.tabletFlag)
            print("Result: " + str(r))

        except Exception,e:
            print("Pepper TableService failed due to:")
            print(e)

    def stopDisplay(self, filename):   
        if(self.tabletFlag == "webview"):
            self.tabletProxy.hideWebview()
            self.tabletFlag = False
        elif(self.tabletFlag == "image"):
            self.tabletProxy.hideImage()
            self.tabletFlag = False
        elif(self.tabletFlag == "video"):
            self.tabletProxy.stopVideo()
            self.tabletFlag = False


if __name__ == '__main__':
    pepper = Pepper_controller(robotIP, PORT)
    
    

