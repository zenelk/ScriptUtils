class Log(object):
	@staticmethod
	def info(message):
		print "INFO: " + message

	@staticmethod
	def warn(message):
		print "WARNING: " + message

	@staticmethod
	def error(message):
		print "ERROR: " + message

	@staticmethod
	def fatal(message):
		print "!!FATAL!! " + message