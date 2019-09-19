#!/usr/bin/env python

from pepper_controller import PepperController


import time

robotIP = "westey.local" #Stevey
PORT = 9559

class SpeechRecog(PepperController):
    
    def startStuff(self):
        self.setVocabulary()
        self.speechRecognition()

    def fudge(self):        
        self.lifeProxy.setState("solitary")
        self.navigationProxy.navigateTo(-0.5,0,0,True)
        self.onWordRecognized()
        #wordRecognized = self.memoryProxy.getData("WordRecognized")
        #if wordRecognized[0] == "Pepper" or wordRecognized[0] == "hi":
        #    self.say("ohai")
        #time.sleep(2)
        #wordRecognized = self.memoryProxy.getData("WordRecognized")
        #if wordRecognized[0] == "Pepper" or wordRecognized[0] == "hi":
        #    self.say("ohai")
            


if __name__ == '__main__':
    task = SpeechRecog(robotIP, PORT)
    task.startStuff()
    task.fudge()
    
