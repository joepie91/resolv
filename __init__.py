import re
from resolvers import *

def resolve(url):
	if re.match("https?:\/\/(www\.)?putlocker\.com", url) is not None:
		return putlocker.resolve(url)
	elif re.match("https?:\/\/(www\.)?sockshare\.com", url) is not None:
		return sockshare.resolve(url)
	else:
		return {}
