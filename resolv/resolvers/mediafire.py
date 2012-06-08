import re, urllib2
from resolv.shared import ResolverError, unescape

def resolve(url):
	try:
		contents = urllib2.urlopen(url).read()
	except:
		raise ResolverError("Could not retrieve the specified URL.")
	
	matches = re.search('kNO = "([^"]+)";', contents)
	
	if matches is None:
		raise ResolverError("No download was found on the given URL; the server for this file may be in maintenance mode, or the given URL may not be valid. It is also possible that you have been blocked - CAPTCHA support is not yet present.")
	
	file_url = matches.group(1)
	
	try:
		file_title = unescape(re.search('<title>([^<]+)<\/title>', contents).group(1))
	except:
		raise ResolverError("Could not find the download title.")
	
	file_dict = {
		'url'		: file_url,
		'priority'	: 1,
		'format'	: "unknown"
	}
	
	return { 'title': file_title, 'files': [file_dict] }
