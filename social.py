from naoqi import ALProxy, ALModule
import time
import thread

#Set IP, Port, and global variables
robotIP = "10.2.0.114"
PORT = 9559	
#vocabulary = ["pepper", "yes"]
	
class PepperController(object):

	def __init__(self, robotIP, PORT):
		self.reinit = False

		self._robotIP = robotIP
		self._PORT = PORT

		#self.session = qi.Session()
		self.setup()

	def setup(self):
		self.lifeProxy = ALProxy("ALAutonomousLife", self._robotIP, self._PORT)
		self.engageProxy = ALProxy("ALEngagementZones", self._robotIP, self._PORT)
		self.peoplePerceptionProxy = ALProxy("ALPeoplePerception", self._robotIP, self._PORT)
		self.gazeProxy = ALProxy("ALGazeAnalysis", self._robotIP, self._PORT)
		self.faceDetectionProxy = ALProxy("ALFaceDetection", self._robotIP, self._PORT)
		self.speechProxy = ALProxy("ALSpeechRecognition", self._robotIP, self._PORT)
		self.soundLocalProxy = ALProxy("ALSoundLocalization", self._robotIP, self._PORT)
		self.soundDetectProxy = ALProxy("ALSoundDetection", self._robotIP, self._PORT)
		self.memoryProxy = ALProxy("ALMemory", self._robotIP, self._PORT)
		self.ttsProxy = ALProxy("ALTextToSpeech", self._robotIP, self._PORT)
		self.trackerProxy = ALProxy("ALTracker", self._robotIP, self._PORT)
		#self.lifeProxy.setState("safeguard")

	def setVocabulary(self):
		self.speechProxy.pause(True)
		self.speechProxy.removeAllContext()
		try:
			self.speechProxy.setLanguage("English")
			self.speechProxy.setVocabulary(["pepper", "yes"],False)
		except:
			print("Vocabulary already set")
		self.speechProxy.pause(False)
		
	def startThread(self):
		thread.start_new_thread(self.onWordRecognized,("words", 2))
		time.sleep(15)
	
	def speechRecognition(self):
		self.memoryProxy.insertData("WordRecognized", " ")
		self.speechProxy.subscribe("attention")
		self.soundLocalProxy.subscribe("soundLocal")
		#self.startThread()
		print "Speech recognition engine started"
		self.onWordRecognized()
		

	def onWordRecognized(self):#, string, threadName):
		heard = False
		while heard == False:
			wordRecognized = self.memoryProxy.getData("WordRecognized")
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
		time.sleep(30)
		self.trackerProxy.stopTracker()
		self.trackerProxy.unregisterAllTargets()
		
	
	def unsubscribe(self):
		self.speechProxy.unsubscribe("attention")
		print "Speech recognition engine stopped"
		
		self.soundLocalProxy.unsubscribe("soundLocal")
		print "Sound localisation stopped"
		
		
		
		
		
		
		
		
		
		
		
		
		