from HTMLParser import HTMLParser
import cookielib, urllib, urllib2

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

class ResolverError(Exception):
	def __init__(self, value):
		self.val = value
		
	def __str__(self):
		return repr(self.val)

class Task():
	captcha = None
	cookiejar = None
	useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11"
	opener = None
	results = None
	state = "none"
	url = ""
	result_type = "none"
	extra_headers = {}
	last_url = ""
	
	def __init__(self, url):
		self.cookiejar = cookielib.CookieJar()
		
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
		self.opener.addheaders = []
		
		self.extra_headers['User-agent'] = self.useragent
		
		for header, payload in self.extra_headers.iteritems():
			self.opener.addheaders.append((header, payload))
		
		self.url = url
	
	def run(self):
		self.state = "finished"
		self.results = self.url
		return self
	
	def fetch_page(self, url):
		request = urllib2.Request(url)
		
		if self.last_url != "":
			request.add_header("Referer", self.last_url)
			
		self.last_url = url
		return self.opener.open(request).read()
	
	def post_page(self, url, data):
		payload = urllib.urlencode(data)
		request = urllib2.Request(url, payload)
		
		if self.last_url != "":
			request.add_header("Referer", self.last_url)
			
		self.last_url = url
		return self.opener.open(request).read()

class Captcha():
	image = ""
	audio = ""
	
	def __init__(image="", audio=""):
		self.image = image
		self.audio = audio

def unescape(s):
	return HTMLParser.unescape.__func__(HTMLParser, s)
