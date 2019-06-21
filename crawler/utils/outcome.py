# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

class Outcome(object):
	def __init__(self, arg):
		self.arg = arg

class OutcomeManager(object):
	def __init__(self):
		self.spider = None

	def start(self, spider):
		self.spider = spider

	def store(self, outcome):
		pass

	def close(self):
		pass