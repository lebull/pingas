import subprocess
import re

import plogger
logger = plogger.initLogger()

class PingResult(object):
	def __init__(self):
	
		self.address = ""
		
		self.success = False
		
		self.count = 1
		self.lost = 0
		self.minimum = None
		self.maximum = None
		
		self.replies = []
		
class PingReply(object):
	def __init__(self):
		self.address = ""
		
		self.success = False
		
		self.bytes = 0
		self.time = 0
		self.ttl = 0
		
	def __str__(self):
		return "Bytes: {}\tLatency: {}\t TTL: {}".format(self.bytes, self.time, self.ttl)

	
class SubprocessFactory(object):
	command = "echo Hello World"
	responseMapping = []
	
	@classmethod
	def execute(cls, **kwargs):
		commandFormatted = cls.command.format(**kwargs)
		logger.info('Executing "{}"'.format(commandFormatted))
		response = subprocess.check_output(commandFormatted, shell=True)
		cls.onFinish(response)
	
	@classmethod
	def onFinish(cls, response):
		cls._parseResponse(response)
		
	@classmethod
	def _parseResponse(cls, response):
		
		pr = PingResult()
		
		for line in response.split('\r\n'):
			segmentText = line.strip()
			success = False
			for rule in cls.getResponseMapping():				
				if re.match(rule[0], segmentText):
					rule[1](segmentText)
					success = True
					break
					
			if not success:
				print "~ Unmapped Line{}".format(segmentText)
		
	
	@staticmethod
	def linepattern(pattern, responseMapping):
		def linePatternDecorator(func):
			responseMapping.append((pattern,func))
		return linePatternDecorator
	
	@classmethod
	def getResponseMapping(cls):
		return cls.responseMapping


	
class PingFactory(SubprocessFactory):
	command = 'ping {address} -n {count}'
	responseMapping = []

	@SubprocessFactory.linepattern(r"^$", responseMapping)
	def _blankLine(responseLine):
		return
			
	@SubprocessFactory.linepattern(r"Reply from (.)*", responseMapping)	
	def _handleSuccessfulWindowsPingResponse(responseLine):
		pr = PingReply()
		infos = responseLine.split(":")[1].strip().split(' ')
		for info in infos:
			
			splitInfo = info.split('=')
			name = splitInfo[0]
			value = splitInfo[1]

			if(name == 'bytes'):
				pr.bytes = value
			if(name == 'time'):
				pr.time = value
			if(name == 'TTL'):
				pr.ttl = value
		pr.success = True
		
		print pr

class TestA(SubprocessFactory):
	command = 'echo Test B'
	responseMapping = []
	
	@SubprocessFactory.linepattern(r"^Test A", responseMapping)
	def rightTest(responseLine):
		print "Right one called"
		
	@SubprocessFactory.linepattern(r"^Test B", responseMapping)
	def wrongTest(responseLine):
		print "Wrong one called"

class TestB(SubprocessFactory):
	command = 'echo Test A'
	responseMapping = []
	
	@SubprocessFactory.linepattern(r"^Test A", SubprocessFactory.responseMapping)
	def wrongTest(responseLine):
		print "Wrong one called"
		
	@SubprocessFactory.linepattern(r"^Test B", responseMapping)
	def rightTest(responseLine):
		print "Right one called"
	
if __name__ == "__main__":
	TestA.execute()
	TestB.execute()
	#PingFactory.execute(address = 'www.google.com', count = 4)
	