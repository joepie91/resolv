import re, urllib, urllib2
from resolv.shared import ResolverError

def resolve(url):
	matches = re.search("https?:\/\/(www\.)?pastebin\.com\/([a-zA-Z0-9]+)", url)
	
	if matches is None:
		raise ResolverError("The provided URL is not a valid Pastebin URL.")
	
	paste_id = matches.group(2)
	
	try:
		contents = urllib2.urlopen(url).read()
	except:
		raise ResolverError("Could not retrieve the specified URL. The specified paste may not exist.")
	
	matches = re.search("<h1>([^<]+)</h1>", contents)
	
	if matches is None:
		raise ResolverError("The provided URL is not a valid paste.")
	
	paste_title = urllib.unquote(matches.group(1))
	
	return { 'title': paste_title, 'files': { 'file': "http://pastebin.com/download.php?i=%s" % paste_id } }