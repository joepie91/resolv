import re, urllib2
from resolv.shared import ResolverError, unescape, Task

class PastebinTask(Task):
	result_type = "text"
	
	name = "Pastebin"
	author = "Sven Slootweg"
	author_url = "http://cryto.net/~joepie91"
	
	def run(self):
		matches = re.search("https?:\/\/(www\.)?pastebin\.com\/([a-zA-Z0-9]+)", self.url)
		
		if matches is None:
			self.state = "invalid"
			raise ResolverError("The provided URL is not a valid Pastebin URL.")
		
		paste_id = matches.group(2)
		
		try:
			contents = self.fetch_page(self.url)
		except urllib2.URLError, e:
			self.state = "failed"
			raise ResolverError("Could not retrieve the specified URL. The paste may not exist.")
		
		matches = re.search("<h1>([^<]+)</h1>", contents)
		
		if matches is None:
			self.state = "invalid"
			raise ResolverError("The provided URL is not a valid paste.")
		
		paste_title = unescape(matches.group(1))
		
		resolved = {
			'url'		: "http://pastebin.com/download.php?i=%s" % paste_id,
			'method'	: "GET",
			'priority'	: 1,
			'format'	: "text"
		}
		
		self.results = {
			'title': paste_title,
			'files': [resolved]
		}
		
		self.state = "finished"
		return self
