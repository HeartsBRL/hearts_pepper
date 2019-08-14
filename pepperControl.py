from naoqi import ALProxy
import time
import thread

#Set IP, Port, Colour, and Font
robotIP = "10.2.0.110"
PORT = 9559	
	
class PepperController(object):

	def __init__(self, robotIP, PORT):
		self.reinit = False

		self._robotIP = robotIP
		self._PORT = PORT

		#self.session = qi.Session()
		self.setup()

	def setup(self):
		self.engageProxy = ALProxy("ALEngagementZones", self._robotIP, self._PORT)
		self.peoplePerceptionProxy = ALProxy("ALPeoplePerception", self._robotIP, self._PORT)
		#self.waveDetectProxy = ALProxy("ALWavingDetection", self._robotIP, self._PORT)
		self.gazeProxy = ALProxy("ALGazeAnalysis", self._robotIP, self._PORT)
		self.faceDetectionProxy = ALProxy("ALFaceDetection", self._robotIP, self._PORT)
		self.speechProxy = ALProxy("ALSpeechRecognition", self._robotIP, self._PORT)
		self.soundLocalProxy = ALProxy("ALSoundLocalization", self._robotIP, self._PORT)
		self.soundDetectProxy = ALProxy("ALSoundDetection", self._robotIP, self._PORT)
		self.memoryProxy = ALProxy("ALMemory", self._robotIP, self._PORT)
		self.ttsProxy = ALProxy("ALTextToSpeech", self._robotIP, self._PORT)
		

	def setVocabulary(self):
		self.speechProxy.pause(True)
		self.speechProxy.setLanguage("English")
		vocabulary = ["pepper", "yes"]
		self.speechProxy.setVocabulary(vocabulary, False)
		self.speechProxy.pause(False)
	
	def speechRecogntion(self):
		thread.start_new_thread(self.onWordRecognized,("words", 2))
		self.memoryProxy.insertData("WordRecognized", " ")
		self.speechProxy.subscribe("attention")
		print "Speech recognition engine started"
		time.sleep(20)
        
	def onWordRecognized(self, string, threadName):
		heard = False
		while heard == False:
			wordRecognized = self.memoryProxy.getData("WordRecognized")
			print (wordRecognized)
			if wordRecognized[0] == "pepper":
				heard = True
				self.ttsProxy.say("I heard you")
				self.speechProxy.unsubscribe("attention")
				print "Speech recognition engine stopped"
				
			