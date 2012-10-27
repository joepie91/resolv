import re, base64
from resolv.shared import ResolverError, TechnicalError, Task

class OneChannelTask(Task):
	result_type = "url"
	
	name = "1channel"
	author = "Sven Slootweg"
	author_url = "http://cryto.net/~joepie91"
	
	def run(self):
		matches = re.search("https?:\/\/(www\.)?1channel\.ch\/external\.php\?.*url=([^&]+)", self.url)

		if matches is None:
			self.state = "invalid"
			raise ResolverError("The provided URL is not a valid external 1channel URL.")
		
		try:
			real_url = base64.b64decode(matches.group(2)).strip()
		except TypeError:
			self.state = "failed"
			raise TechnicalError("The provided URL is malformed.")
		
		self.results = { 'url': real_url }
		self.state = "finished"
		return self
