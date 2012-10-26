import resolv, urllib, urllib2, argparse

# TODO:
# http://www.mediafire.com/view/?vxltbkr2l9ycmah => http://www.mediafire.com/?vxltbkr2l9ycmah

suites = {
	'1channel': {
		"1channel + PutLocker (video)": "http://www.1channel.ch/external.php?title=Big+Buck+Bunny&url=aHR0cDovL3d3dy5wdXRsb2NrZXIuY29tL2ZpbGUvOTg3RkVCRjVEQjY0NUUyRQ==&domain=cHV0bG9ja2VyLmNvbQ==&loggedin=0"
	},
	'putlocker': {
		"PutLocker (video)": "http://www.putlocker.com/file/987FEBF5DB645E2E",
		"SockShare (video)": "http://www.sockshare.com/file/88DF2133C85521BD"
	},
	'filebox': {
		"Filebox (video)": "http://www.filebox.com/p0rp8nabrcfk"
	},
	'pastebin': {
		"Pastebin": "http://pastebin.com/imyEc26g"
	},
	'mediafire': {
		"MediaFire": "http://www.mediafire.com/?vxltbkr2l9ycmah",
		"MediaFire with password (mfddl)": "http://www.mediafire.com/?traa1p0lki9611h"
	},
	'youtube': {
		"YouTube": "http://www.youtube.com/watch?v=XSGBVzeBUbk"
	}
}

parser = argparse.ArgumentParser(description='Testing script for the resolv library.')

parser.add_argument('suites', metavar='SUITE', type=str, nargs='*',
                   help='suites to test (leave empty to test all suites)')

args = parser.parse_args()
options = vars(args)

to_test = {}

if len(options['suites']) == 0:
	for key, suite in suites.iteritems():
		for description, url in suite.iteritems():
			to_test[description] = url
else:
	for suite in options['suites']:
		for description, url in suites[suite].iteritems():
			to_test[description] = url

def process_result(res):
	if res.state == "finished":
		print "Successful!\nType: %s\nResults: %s\nCookie jar: %s" % (res.result_type, str(res.results), str(res.cookiejar))
	elif res.state == "failed":
		print "Failed."
	elif res.state == "invalid":
		print "Invalid URL."
	elif res.state == "need_password":
		pw = raw_input("Password required. Enter password: ")
		res.verify_password(pw)
		process_result(res)
	elif res.state == "password_invalid":
		pw = raw_input("Password invalid! Try again: ")
		res.verify_password(pw)
		process_result(res)
	else:
		print "Unknown result state: %s" % res.state

for title, url in to_test.iteritems():
	print "============ %s ============" % title
	print "RESOLVE:"
	res = resolv.resolve(url)
	process_result(res)
	print ""
	print "RECURSE:"
	res = resolv.recurse(url)
	process_result(res)
	print ""
	
