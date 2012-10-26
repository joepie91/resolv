import re, urllib2
from resolv.shared import ResolverError, unescape, Task

class MediafireTask(Task):
	result_type = "file"
	
	def run(self):
		try:
			contents = self.fetch_page(self.url)
		except urllib2.URLError, e:
			self.state = "failed"
			raise ResolverError("Could not retrieve the specified URL.")
		
		matches = re.search('kNO = "([^"]+)";', contents)
		
		if matches is None:
			self.state = "failed"
			raise ResolverError("No download was found on the given URL; the server for this file may be in maintenance mode, or the given URL may not be valid. It is also possible that you have been blocked - CAPTCHA support is not yet present.")
		
		file_url = matches.group(1)
		
		try:
			file_title = unescape(re.search('<title>([^<]+)<\/title>', contents).group(1))
		except:
			self.state = "failed"
			raise ResolverError("Could not find the download title.")
		
		file_dict = {
			'url'		: file_url,
			'priority'	: 1,
			'format'	: "unknown"
		}
		
		self.results = {
			'title': file_title,
			'files': [file_dict]
		}
		
		self.state = "finished"
		return self
