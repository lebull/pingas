import subprocess


class PingResult(object):
	def __init__(self):
		self.target = ""
		self.success = False
		self.count = 1
		self.lost = 0
		self.minimum = None
		self.maximum = None
		self.replies = []
		
class PingReply(object)
	def __init__(self):
		self.target = ""
		self.bytes = 0
		self.time = 0
		self.ttl = 0
		
		
if __name__ == "__main__":
	command = 'ping www.google.com'
	print subprocess.check_output(command)
	
	