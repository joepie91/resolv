from HTMLParser import HTMLParser
import cookielib, urllib, urllib2, re

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

class ResolverError(Exception):
	def __init__(self, value):
		self.val = value
		
	def __str__(self):
		return repr(self.val)
		
class TechnicalError(Exception):
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
		
	def verify_password(password):
		# Has to be overridden by inherited classes.
		pass
		
	def verify_image_captcha(solution):
		# Has to be overridden by inherited classes.
		pass
		
	def verify_audio_captcha(solution):
		# Has to be overridden by inherited classes.
		pass
		
	def verify_text_captcha(solution):
		# Has to be overridden by inherited classes.
		pass

class Captcha():
	image = None
	audio = None
	text = None
	task = None
	
	def __init__(self, task, image=None, audio=None, text=None):
		self.image = image
		self.audio = audio
		self.text = text
		self.task = task
	
	def get_image(self):
		return self.task.fetch_page(self.image)
	
	def get_audio(self):
		return self.task.fetch_page(self.audio)

def unescape(s):
	return HTMLParser.unescape.__func__(HTMLParser, s)

def str_base(num, base):
	# Thanks to http://code.activestate.com/recipes/65212/#c7
	return ((num == 0) and  "0" ) or ( str_base(num // base, base).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % base])

def unpack_js(packed):
	positions = re.search("return p\}\('(.+[^\\\\])',", packed).group(1)
	base, counter, strings = re.search(",([0-9]+),([0-9]+),'([^']+)'", packed).groups(1)

	counter = int(counter)
	base = int(base)
	strings = strings.split("|")

	for i in reversed(xrange(0, int(counter))):
		target = str_base(i, base)
		positions = re.sub(r"\b%s\b" % target, strings[i], positions)
	
	# Fix escaped apostrophes.
	positions = re.sub(r"(?<!\\)\\'", "'", positions)
	
	return positions
