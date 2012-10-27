import re
from resolv.shared import ResolverError, TechnicalError, unescape, Task

class PutlockerTask(Task):
	result_type = "video"
	
	name = "PutLocker"
	author = "Sven Slootweg"
	author_url = "http://cryto.net/~joepie91"
	
	def run(self):
		try:
			import mechanize
		except ImportError:
			self.state = "failed"
			raise TechnicalError("The Python mechanize module is required to resolve PutLocker URLs.")
		
		matches = re.search("https?:\/\/(www\.)?putlocker\.com\/(file|embed)\/([A-Z0-9]+)", self.url)

		if matches is None:
			self.state = "invalid"
			raise ResolverError("The provided URL is not a valid PutLocker URL.")
		
		video_id = matches.group(3)
		
		try:
			browser = mechanize.Browser()
			browser.set_handle_robots(False)
			browser.open("http://putlocker.com/embed/%s" % video_id)
		except:
			self.state = "failed"
			raise TechnicalError("The PutLocker site could not be reached.")
		
		try:
			browser.select_form(nr=0)
			result = browser.submit()
			page = result.read()
		except Exception, e:
			self.state = "nonexistent"
			raise ResolverError("The file was removed, or the URL is incorrect.")
			
		matches = re.search("playlist: '([^']+)'", page)
		
		if matches is None:
			self.state = "failed"
			raise ResolverError("No playlist was found on the given URL; the PutLocker server for this file may be in maintenance mode, or the given URL may not be a video file. The PutLocker resolver currently only supports video links.")
		
		playlist = matches.group(1)
		
		try:
			browser.open("http://www.putlocker.com%s" % playlist)
		except:
			self.state = "failed"
			raise TechnicalError("The playlist file for the given URL could not be loaded.")
		
		matches = re.search("url=\"([^\"]+)\" type=\"video\/x-flv\"", browser.response().read())
		
		if matches is None:
			self.state = "failed"
			raise ResolverError("The playlist file does not contain any video URLs. The PutLocker resolver currently only supports video links.")
		
		video_file = matches.group(1)
		
		try:
			video_title = unescape(re.search('<a href="\/file\/[^"]+"[^>]*><strong>([^<]*)<\/strong><\/a>', page).group(1))
		except:
			self.state = "failed"
			raise TechnicalError("Could not find the video title.")
		
		stream_dict = {
			'url'		: video_file,
			'method'	: "GET",
			'quality'	: "unknown",
			'priority'	: 1,
			'format'	: "unknown"
		}
		
		self.results = {
			'title': video_title,
			'videos': [stream_dict]
		}
		
		self.state = "finished"
		return self
