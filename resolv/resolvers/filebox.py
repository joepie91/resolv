import re, time, urllib2
from resolv.shared import ResolverError

def resolve(url):
	matches = re.search("https?:\/\/(www\.)?filebox\.com\/([a-zA-Z0-9]+)", url)
	
	if matches is None:
		raise ResolverError("The provided URL is not a valid Filebox.com URL.")
	
	video_id = matches.group(2)
	
	try:
		contents = urllib2.urlopen("http://www.filebox.com/embed-%s-970x543.html" % video_id).read()
	except:
		raise ResolverError("Could not retrieve the video page.")
	
	matches = re.search("url: '([^']+)',", contents)
	
	if matches is None:
		raise ResolverError("No video was found on the specified URL.")
	
	video_file = matches.group(1)
	
	return { 'title': "", 'videos': { 'video': video_file } }
	
def resolve2(url):
	# This is a fallback function in case no video could be found through the resolve() method.
	# It's not recommended to use it, as it introduces a 5 second wait.
	
	try:
		import mechanize
	except ImportError:
		raise ResolverError("The Python mechanize module is required to resolve Filebox.com URLs.")
	
	matches = re.search("https?:\/\/(www\.)?filebox\.com\/([a-zA-Z0-9]+)", url)

	if matches is None:
		raise ResolverError("The provided URL is not a valid Filebox.com URL.")
	
	try:
		browser = mechanize.Browser()
		browser.set_handle_robots(False)
		browser.open(url)
	except:
		raise ResolverError("The Filebox.com site could not be reached.")
	
	time.sleep(6)
	
	try:
		browser.select_form(nr=0)
		result = browser.submit()
		page = result.read()
	except Exception, e:
		raise ResolverError("The file was removed, or the URL is incorrect.")
	
	matches = re.search("this\.play\('([^']+)'\)", page)
	
	if matches is None:
		raise ResolverError("No video file was found on the given URL; the Filebox.com server for this file may be in maintenance mode, or the given URL may not be a video file. The Filebox.com resolver currently only supports video links.")
	
	video_file = matches.group(1)
	
	return { 'title': "", 'videos': { 'video': video_file } }
