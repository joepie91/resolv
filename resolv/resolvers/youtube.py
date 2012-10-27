import re, urllib, urllib2, urlparse
from resolv.shared import ResolverError, TechnicalError, unescape, Task

class YoutubeTask(Task):
	result_type = "video"
	
	name = "YouTube"
	author = "Sven Slootweg"
	author_url = "http://cryto.net/~joepie91"
	
	extra_headers = {
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-us,en;q=0.5'
	}
	
	def run(self):
		try:
			contents = self.fetch_page(self.url)
		except urllib2.URLError, e:
			self.state = "failed"
			raise TechnicalError("Could not retrieve the specified URL.")
		
		if '<meta property="og:video:type"' not in contents:
			self.state = "invalid"
			raise ResolverError("The specified URL is not a valid YouTube video.")
		
		map_start = "url_encoded_fmt_stream_map="
		map_end = "\\u0026amp;"
		
		try:
			pos_start = contents.index(map_start) + len(map_start)
			snippet = contents[pos_start:]
		except ValueError:
			self.state = "failed"
			raise TechnicalError("The starting position for the YouTube player configuration could not be found. Is the URL really a valid video page?")
		
		try:
			pos_end = snippet.index(map_end)
			stream_map = snippet[:pos_end]
		except ValueError:
			self.state = "failed"
			raise TechnicalError("The ending position for the YouTube player configuration could not be found.")
		
		try:
			stream_map = urllib.unquote(stream_map)
			streams = stream_map.split(',')
		except:
			self.state = "failed"
			raise TechnicalError("The YouTube player configuration is corrupted.")
		
		stream_pool = []
		
		for stream in streams:
			fields = urlparse.parse_qs(stream)
			
			if len(fields) < 6:
				self.state = "failed"
				raise TechnicalError("The amount of fields in the YouTube player configuration is incorrect.")
			
			signature = fields['sig'][0]
			video_url = "%s&signature=%s" % (fields['url'][0], signature)
			quality = fields['quality'][0]
			fallback_host = fields['fallback_host'][0]
			mimetype = fields['type'][0]
			itag = fields['itag'][0]
			
			if mimetype.startswith("video/mp4"):
				video_format = "mp4"
			elif mimetype.startswith("video/x-flv"):
				video_format = "flv"
			elif mimetype.startswith("video/3gpp"):
				video_format = "3gp"
			elif mimetype.startswith("video/webm"):
				video_format = "webm"
			else:
				video_format = "unknown"
			
			if quality == "small":
				video_quality = "240p"
				video_priority = 5
			elif quality == "medium":
				video_quality = "360p"
				video_priority = 4
			elif quality == "large":
				video_quality = "480p"
				video_priority = 3
			elif quality == "hd720":
				video_quality = "720p"
				video_priority = 2
			elif quality == "hd1080":
				video_quality = "1080p"
				video_priority = 1
			else:
				video_quality = "unknown"
				video_priority = 10
				print "UNKNOWN: %s" % quality
			
			stream_dict = {
				'url'		: video_url,
				'method'	: "GET",
				'quality'	: video_quality,
				'priority'	: video_priority,
				'format'	: video_format,
				'extra'		: {
					'itag':			itag,
					'mimetype':		mimetype,
					'fallback_host':	fallback_host
				}
			}
			
			stream_pool.append(stream_dict)
		
		try:
			video_title = unescape(re.search('<meta property="og:title" content="([^"]*)">', contents).group(1))
		except:
			self.state = "failed"
			raise TechnicalError("Could not find the video title.")
		
		self.results = {
			'title': video_title,
			'videos': stream_pool
		}
		
		self.state = "finished"
		return self
