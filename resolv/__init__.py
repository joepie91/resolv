import re
import resolvers

from resolv.shared import ResolverError

def resolve(url):
	if re.match("https?:\/\/(www\.)?putlocker\.com", url) is not None:
		task = resolvers.PutlockerTask(url)
		return task.run()
	elif re.match("https?:\/\/(www\.)?sockshare\.com", url) is not None:
		task = resolvers.SockshareTask(url)
		return task.run()
	elif re.match("https?:\/\/(www\.)?1channel\.ch\/external\.php", url) is not None:
		task = resolvers.OneChannelTask(url)
		return task.run()
	elif re.match("https?:\/\/(www\.)?youtube\.com\/watch\?", url) is not None:
		task = resolvers.YoutubeTask(url)
		return task.run()
	elif re.match("https?:\/\/(www\.)?filebox\.com\/[a-zA-Z0-9]+", url) is not None:
		task = resolvers.FileboxTask(url)
		return task.run()
	elif re.match("https?:\/\/(www\.)?vidxden\.com\/[a-zA-Z0-9]+", url) is not None:
		task = resolvers.VidxdenTask(url)
		return task.run()
	elif re.match("https?:\/\/(www\.)?vidbux\.com\/[a-zA-Z0-9]+", url) is not None:
		task = resolvers.VidbuxTask(url)
		return task.run()
	elif re.match("https?:\/\/(www\.)?filenuke\.com\/[a-zA-Z0-9]+", url) is not None:
		task = resolvers.FilenukeTask(url)
		return task.run()
	elif re.match("https?:\/\/(www\.)?pastebin\.com\/[a-zA-Z0-9]+", url) is not None:
		task = resolvers.PastebinTask(url)
		return task.run()
	elif re.match("https?:\/\/(www\.)?mediafire\.com\/(view\/)?\?[a-z0-9]+", url) is not None:
		task = resolvers.MediafireTask(url)
		return task.run()
	else:
		raise ResolverError("No suitable resolver found for %s" % url)

def recurse(url):
	previous_result = {}
	
	while True:
		result = resolve(url)
		
		if result.state == "failed":
			return previous_result
		elif result.result_type != "url":
			return result
		
		url = result.results['url']
		previous_result = result
