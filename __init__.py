import re
from resolvers import *

def resolve(url):
	if re.match("https?:\/\/(www\.)?putlocker\.com", url) is not None:
		return putlocker.resolve(url)
	elif re.match("https?:\/\/(www\.)?sockshare\.com", url) is not None:
		return sockshare.resolve(url)
	elif re.match("https?:\/\/(www\.)?1channel\.ch\/external\.php", url) is not None:
		return onechannel.resolve(url)
	elif re.match("https?:\/\/(www\.)?youtube\.com\/watch\?", url) is not None:
		return youtube.resolve(url)
	elif re.match("https?:\/\/(www\.)?filebox\.com\/[a-zA-Z0-9]+", url) is not None:
		return filebox.resolve(url)
	elif re.match("https?:\/\/(www\.)?pastebin\.com\/[a-zA-Z0-9]+", url) is not None:
		return pastebin.resolve(url)
	else:
		return {}

def recurse(url):
	previous_result = {}
	
	while True:
		result = resolve(url)
		
		if result == {}:
			return previous_result
		elif 'url' not in result:
			return result
		
		url = result['url']
		previous_result = result
