import re, base64
from resolv.shared import ResolverError

def resolve(url):
	matches = re.search("https?:\/\/(www\.)?1channel\.ch\/external\.php\?.*url=([^&]+)", url)

	if matches is None:
		raise ResolverError("The provided URL is not a valid external 1channel URL.")
	
	try:
		real_url = base64.b64decode(matches.group(2)).strip()
	except TypeError:
		raise ResolverError("The provided URL is malformed.")
	
	return { 'url': real_url }
