from HTMLParser import HTMLParser

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

class ResolverError(Exception):
	def __init__(self, value):
		self.val = value
		
	def __str__(self):
		return repr(self.val)

def unescape(s):
	return HTMLParser.unescape.__func__(HTMLParser, s)
