import re
from resolvers import *

def resolve(url):
	if re.match("https?:\/\/(www\.)?putlocker\.com", url) is not None:
		return putlocker.resolve(url)
	elif re.match("https?:\/\/(www\.)?sockshare\.com", url) is not None:
		return sockshare.resolve(url)
	elif re.match("https?:\/\/(www\.)?1channel\.ch\/external\.php", url) is not None:
		return onechannel.resolve(url)
	else:
		return {}

def recurse(url):
	while True:
		result = resolve(url)
		
		if 'url' not in result:
			return result
		
		url = result['url']
