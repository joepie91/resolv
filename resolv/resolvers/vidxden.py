import re, time, urllib2
from resolv.shared import ResolverError, TechnicalError, Task, unpack_js

# No such file or the file has been removed due to copyright infringement issues.

class VidxdenTask(Task):
	result_type = "video"
	
	name = "VidX Den"
	author = "Sven Slootweg"
	author_url = "http://cryto.net/~joepie91"
	
	def run(self):
		matches = re.search("https?:\/\/(www\.)?vidxden\.com\/([a-zA-Z0-9]+)", self.url)
		
		if matches is None:
			self.state = "invalid"
			raise ResolverError("The provided URL is not a valid VidX Den URL.")
		
		video_id = matches.group(2)
		
		try:
			contents = self.fetch_page(self.url)
		except urllib2.URLError, e:
			self.state = "failed"
			raise TechnicalError("Could not retrieve the video page.")
		
		if 'Human Verification' not in contents:
			self.state = "invalid"
			raise ResolverError("The provided URL does not exist.")
		
		matches = re.search('<input name="fname" type="hidden" value="([^"]+)">', contents)
		
		if matches is None:
			self.state = "failed"
			raise TechnicalError("Could not find filename.")
			
		filename = matches.group(1)
		
		matches = re.search('<input name="referer" type="hidden" value="([^"]*)">', contents)
		
		if matches is None:
			self.state = "failed"
			raise TechnicalError("Could not find referer.")
			
		referer = matches.group(1)
		
		try:
			contents = self.post_page(self.url, {
				'op': 		"download1",
				'usr_login':	"",
				'id':		video_id,
				'filename':	filename,
				'referer':	referer,
				'method_free':	"Continue to Video"
			})
		except urllib2.URLError, e:
			self.state = "failed"
			raise TechnicalError("Could not complete human verification")
		
		script = unpack_js(contents)
		
		matches = re.search("'file','([^']+)'", script)
		
		if matches is None:
			self.state = "failed"
			raise TechnicalError("No video was found on the specified URL.")
		
		video_file = matches.group(1)
		
		stream_dict = {
			'url'		: video_file,
			'method'	: "GET",
			'quality'	: "unknown",
			'priority'	: 1,
			'format'	: "unknown"
		}
		
		self.results = {
			'title': "",
			'videos': [stream_dict]
		}
		
		self.state = "finished"
		return self
