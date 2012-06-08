class ResolverError(Exception):
	def __init__(self, value):
		self.val = value
		
	def __str__(self):
		return repr(self.val)
