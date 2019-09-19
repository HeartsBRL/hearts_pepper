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
        self.moveHere(0.5,0,0,True)
        self.onWordRecognized()


if __name__ == '__main__':
    task = SpeechRecog(robotIP, PORT)
    task.startStuff()
    task.fudge()
    
