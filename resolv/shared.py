class ResolverError(Exception):
	def __init__(self, value):
		self.val = value
		
	def __str__(self):
		return repr(self.val)

def unescape(s):
	s = s.replace("&lt;", "<")
	s = s.replace("&gt;", ">")
	s = s.replace("&quot;", '"')
	s = s.replace("&apos;", "'")
	s = s.replace("&amp;", "&")
	return s
