from naoqi import ALProxy, ALModule
import time
import thread

#Set IP, Port, and global variables
robotIP = "10.2.0.114"
PORT = 9559	
#listening = True
vocabulary = ["pepper", "yes"]
	
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
		self.speechProxy.removeAllContext()
		try:
			self.speechProxy.setLanguage("English")
			self.speechProxy.setVocabulary(vocabulary,False)
		except:
			print("Vocabulary already set")
		self.speechProxy.pause(False)
	
	def speechRecogntion(self):
		#global listening
		#while listening == True:
		thread.start_new_thread(self.onWordRecognized,("words", 2))
		self.memoryProxy.insertData("WordRecognized", " ")
		self.memoryProxy.insertData("SoundLocated", " ")
		self.speechProxy.subscribe("attention")
		self.soundLocalProxy.subscribe("soundLocal")
		#self.soundDetectProxy.subscribe("attention")
		print "Speech recognition engine started"
		time.sleep(15)
		

	def onWordRecognized(self, string, threadName):
		#global listening
		heard = False
		while heard == False:
			wordRecognized = self.memoryProxy.getData("WordRecognized")
			print (wordRecognized)
			if wordRecognized[0] == "pepper":
			#if "pepper" in wordRecognized:
				heard = True
				#listening = False
				#soundDetected = self.memoryProxy.getData("SoundDetected")
				#print(soundDetected)
				
				soundLocated = self.memoryProxy.subscribeToMicroEvent("SoundLocated", "ALSoundLocalization", "Sound located", "self.unSubscribe")
				location = self.memoryProxy.getData("SoundLocated")
				
				self.unSubscribe()
				print("soundLocated", location)
				
				#action
				#self.ttsProxy.say("I heard you")
				

				#self.soundDetectProxy.unsubscribe("attention")
				
		
	def unSubscribe(self):
		#unsubscribe
		self.speechProxy.unsubscribe("attention")
		print "Speech recognition engine stopped"
		
		self.memoryProxy.unsubscribeToMicroEvent("SoundLocated", "ALSoundLocalization")
		print "MicroEvent unSubscribed"

		self.soundLocalProxy.unsubscribe("soundLocal")
		print "Sound localisation engine stopped"

		
		
		
		
		
		
		
		
		
		
		
		