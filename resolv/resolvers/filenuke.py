import re, time, urllib2
from resolv.shared import ResolverError, TechnicalError, Task, unpack_js

# No such file or the file has been removed due to copyright infringement issues.

class FilenukeTask(Task):
	result_type = "video"
	
	name = "Filenuke"
	author = "Sven Slootweg"
	author_url = "http://cryto.net/~joepie91"
	
	def run(self):
		matches = re.search("https?:\/\/(www\.)?filenuke\.com\/([a-zA-Z0-9]+)", self.url)
		
		if matches is None:
			self.state = "invalid"
			raise ResolverError("The provided URL is not a valid Filenuke URL.")
		
		video_id = matches.group(2)
		
		try:
			contents = self.fetch_page(self.url)
		except urllib2.URLError, e:
			self.state = "failed"
			raise TechnicalError("Could not retrieve the video page.")
		
		if 'Choose how to download' not in contents:
			self.state = "invalid"
			raise ResolverError("The provided URL does not exist.")
		
		matches = re.search('<input type="hidden" name="fname" value="([^"]+)">', contents)
		
		if matches is None:
			self.state = "failed"
			raise TechnicalError("Could not find filename.")
			
		filename = matches.group(1)
		
		matches = re.search('<input type="hidden" name="referer" value="([^"]*)">', contents)
		
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
				'method_free':	"Free"
			})
		except urllib2.URLError, e:
			self.state = "failed"
			raise TechnicalError("Could not continue to download")
		
		matches = re.search('<div id="player_code">(.*?)</div>', contents, re.DOTALL)
		
		if matches is None:
			self.state = "unsupported"
			raise ResolverError("No player was found. The Filenuke resolver currently only supports video links.")
		
		player_code = matches.group(1)
		
		script = unpack_js(player_code)
		
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
