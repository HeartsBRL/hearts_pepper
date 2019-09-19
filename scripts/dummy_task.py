#!/usr/bin/env python

from pepperControl import PepperController
import thread

robotIP = "10.2.0.110" #Stevey
PORT = 9559

class DummyTask(PepperController):

    def work(self):
        self.say("boop")


if __name__ == '__main__':
    dummy = DummyTask(robotIP, PORT)
    dummy.setVocabulary()
    dummy.speechRecogntion()