#!/usr/bin/env python

from pepper_controller import PepperController


import time

robotIP = "westey.local" #Stevey
PORT = 9559

class SpeechRecog(PepperController):
    
    def fudge(self):
        self.setVocabulary()
        self.lifeProxy.setState("solitary")
        self.speechRecognition()
        self.moveHere(0.5,0,0,True)
        self.onWordRecognized()


if __name__ == '__main__':
    task = SpeechRecog(robotIP, PORT)
    task.fudge()
    
