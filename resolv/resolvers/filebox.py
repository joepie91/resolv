import re, time, urllib2
from resolv.shared import ResolverError, TechnicalError, Task

class FileboxTask(Task):
	result_type = "video"
	
	name = "Filebox.com"
	author = "Sven Slootweg"
	author_url = "http://cryto.net/~joepie91"
	
	def run(self):
		matches = re.search("https?:\/\/(www\.)?filebox\.com\/([a-zA-Z0-9]+)", self.url)
		
		if matches is None:
			self.state = "invalid"
			raise ResolverError("The provided URL is not a valid Filebox.com URL.")
		
		video_id = matches.group(2)
		
		try:
			contents = self.fetch_page("http://www.filebox.com/embed-%s-970x543.html" % video_id)
		except urllib2.URLError, e:
			self.state = "failed"
			raise TechnicalError("Could not retrieve the video page.")
		
		matches = re.search("url: '([^']+)',", contents)
		
		if matches is None:
			self.state = "invalid"
			raise ResolverError("No video was found on the specified URL. The Filebox.com resolver currently only supports videos.")
		
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
