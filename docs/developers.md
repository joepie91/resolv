# Documentation for developers

The majority of this document will apply to both third-party developers ("users") of the resolv library, and core/plugin developers writing code for resolv itself. Where necessary, a distinction is made using the terms "users" (for third-party developers that use resolv in their project as a library) and "developers" (for developers that work on either the core or the plugins for the resolv library).

## Purpose

The purpose of python-resolv is quite simple: to provide a reusable library for resolving URLs. "Resolving" in this context refers to various things; for example:

 * The resolution of an obfuscated 'external' 1channel URL to the real URL of a stream.
 * The resolution of a YouTube URL to directly streamable video files that can for example be downloaded via wget, or streamed via VLC Media Player (in various qualities).
 * The resolution of a Mediafire page URL to a wget-able direct URL.
 * The resolution of a Pastebin URL to a 'raw' version, including the fetching of the title.
 * And so on, and so on...

Basically, resolv's purpose is to turn any kind of URL into the most 'direct' URL that can be acquired for either streaming or downloading, in such a way that it can easily be integrated into third-party software (such as a download manager, media player, etc.)

## Technical summary

The resolv library is a Python module - this means it can be imported like any other module and used in any Python application or application that supports Python scripting. Each "resolver" - a 'plugin' to resolve URLs for a certain service - is its own class, inheriting from the Task base class. A task may either be finished immediately, or require further user input (for example, a password or a CAPTCHA solution). The final result is a nested dictionary with the information that is necessary for downloading or streaming. The library can be kept up to date independently via its PyPi packages.

## Currently supported services:

<table>
	<tr>
		<th>Name</th>
		<th>Supported URL types</th>
		<th>Supports CAPTCHAs</th>
		<th>Class name</th>
	</tr>
	<tr>
		<td>Pastebin</td>
		<td>All URLs</td>
		<td>n/a</td>
		<td>PastebinTask</td>
	</tr>
	<tr>
		<td>YouTube</td>
		<td>All URLs</td>
		<td>No</td>
		<td>YoutubeTask</td>
	</tr>
	<tr>
		<td>Mediafire</td>
		<td>Files, password-protected files</td>
		<td>No</td>
		<td>MediafireTask</td>
	</tr>
	<tr>
		<td>PutLocker</td>
		<td>Videos</td>
		<td>n/a</td>
		<td>PutlockerTask</td>
	</tr>
	<tr>
		<td>SockShare</td>
		<td>Videos</td>
		<td>n/a</td>
		<td>SockshareTask</td>
	</tr>
	<tr>
		<td>FileBox.com</td>
		<td>Videos</td>
		<td>n/a</td>
		<td>FileboxTask</td>
	</tr>
	<tr>
		<td>1channel</td>
		<td>Obfuscated external URLs</td>
		<td>n/a</td>
		<td>OneChannelTask</td>
	</tr>
	<tr>
		<td>VidX Den</td>
		<td>All URLs</td>
		<td>n/a</td>
		<td>VidxdenTask</td>
	</tr>
	<tr>
		<td>VidBux</td>
		<td>All URLs</td>
		<td>n/a</td>
		<td>VidbuxTask</td>
	</tr>
	<tr>
		<td>Filenuke</td>
		<td>Videos</td>
		<td>n/a</td>
		<td>FilenukeTask</td>
	</tr>
</table>

## Getting started

To install resolv, you can use `pip install resolv` or the PyPi-using package manager of your choice. To update resolve, run `pip install --upgrade resolv`.

To start using the resolv library in your code (or in a Python shell), simply `import resolv`.

## Resolving

The resolv library can be used in two ways: either by using a specific resolver directly, or by letting the library figure out what resolver to use for a URL.

### Automatically detecting the needed resolver

If you want to have the library automatically figure out what resolver to use, there are two functions available for you that only differ slightly:

#### resolv.resolve(url)
*Returns:* an instance of a Task-derived class, depending on the resolver used.

This function finds the needed resolver, attempts to complete resolution, and returns the newly created task.

Example:

	>>> import resolv
	>>> task = resolv.resolve("http://www.1channel.ch/external.php?title=Big+Buck+Bunny&url=aHR0cDovL3d3dy5wdXRsb2NrZXIuY29tL2ZpbGUvOTg3RkVCRjVEQjY0NUUyRQ==&domain=cHV0bG9ja2VyLmNvbQ==&loggedin=0")
	>>> task.state
	'finished'
	>>> task.results
	{'url': 'http://www.putlocker.com/file/987FEBF5DB645E2E'}

#### resolv.recurse(url)
*Returns:* an instance of a Task-derived class, depending on the resolver used.

This function does the same as resolv.resolve(), but will only return the result if it is not a deobfuscated URL, or if the 'next hop' failed to resolve. This means that, for example, running resolv.recurse() on an obfuscated 1channel link will not return the URL behind that obfuscated link, but a *resolved* version of that URL.

Example:

	>>> import resolv
	>>> task = resolv.recurse("http://www.1channel.ch/external.php?title=Big+Buck+Bunny&url=aHR0cDovL3d3dy5wdXRsb2NrZXIuY29tL2ZpbGUvOTg3RkVCRjVEQjY0NUUyRQ==&domain=cHV0bG9ja2VyLmNvbQ==&loggedin=0")
	>>> task.state
	'finished'
	>>> task.results
	{'videos': [{'url': "http://media-a9.putlocker.com/download/41/1246281_61c1d.flv?h=fMVE5HhbDbqv_WuXJZHSXw&amp;e=1351276025&amp;f='1246281_61c1d.flv'", 'priority': 1, 'quality': 'unknown', 'method': 'GET', 'format': 'unknown'}], 'title': 'Big Buck Bunny 39'}

### Manually picking a resolver

If you wish to only resolve a certain type of URL, you can manually pick a resolver for a certain site. Simply create a new instance of resolv.resolvers.*classname* with the target URL as argument, and call the run() method.

Let's say that we want to, for example, resolve a specific Putlocker URL. We would do this:

	>>> import resolv
	>>> task = resolv.resolvers.PutlockerTask("http://www.putlocker.com/file/987FEBF5DB645E2E")
	>>> task.run()
	>>> task.state
	'finished'
	>>> task.results
	{'videos': [{'url': "http://media-a9.putlocker.com/download/41/1246281_61c1d.flv?h=OFwiLT3SwZxenCNEt5650g&amp;e=1351276212&amp;f='1246281_61c1d.flv'", 'priority': 1, 'quality': 'unknown', 'method': 'GET', 'format': 'unknown'}], 'title': 'Big Buck Bunny 39'}

It's really that simple!

## Catching exceptions

All user-related exceptions (deleted files, and such) thrown by the resolv module are `resolv.shared.ResolverError` exceptions. It's recommended to do the following to make error-catching easier:

	from resolv.shared import ResolverError

After doing this, you can simply refer to `ResolverError` directly, instead of `resolv.shared.ResolverError`.

The error message will always have a user-friendly description explaining what went wrong. It is feasible to directly show these error messages to the end user when they occur.

In a similar way, `resolv.shared.TechnicalError` is used for technical failures that are likely to indicate a broken resolver.

Technical errors should typically be logged, and a generic 'broken' message should be shown to the user.

## Dealing with results

The run() method will return the relevant task (this will usually be itself, although it is technically possible to create a new task and return that instead). This instance of a Task-derived class will have certain information and functions available.

### Task.name

The name of the resolver. This is usually the name of the site.

### Task.author

The author of the resolver.

### Task.author_url

The URL for this resolver (this will typically be the site of the author, a repository, etc.)

### Task.state

The state that the task is in - this is guaranteed to be set after calling run(). The state may be any of the following:

<table>
	<tr>
		<th>Name</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>blank</td>
		<td>The run() method has not been called yet.</td>
	</tr>
	<tr>
		<td>finished</td>
		<td>The URL was successfully resolved.</td>
	</tr>
	<tr>
		<td>need_password</td>
		<td>A password is required to resolve this URL.</td>
	</tr>
	<tr>
		<td>password_invalid</td>
		<td>The provided password was incorrect.</td>
	</tr>
	<tr>
		<td>need_captcha</td>
		<td>A CAPTCHA needs to be solved to continue resolving.</td>
	</tr>
	<tr>
		<td>captcha_invalid</td>
		<td>The given CAPTCHA response was incorrect.</td>
	</tr>
	<tr>
		<td>invalid</td>
		<td>The URL is invalid for this resolver.</td>
	</tr>
	<tr>
		<td>unsupported</td>
		<td>This type of URL is not supported by this resolver.</td>
	</tr>
	<tr>
		<td>failed</td>
		<td>The resolution failed for some other reason.</td>
	</tr>
</table>

How to handle these situations is up to your application.

### Task.result_type

This variable holds the type of result that the Task holds. It can be any of `url` (for deobfuscated and un-shortened URLs), `file` (for downloadable files), `text` (for pastebins and such), `video` (for streaming video), `audio` (for streaming audio), and `image` for embeddable images. A special type is `dummy` which is used by the `dummy` resolver, but may also appear in other resolvers for testing purposes. For all practical purposes, `dummy` results should be ignored.

__Important:__ Do *not* use this variable to determine whether resolution was successful. A resolver may set this variable before doing any resolution, if the resolver only supports one kind of result.

### Task.results

This variable holds the results of the resolution. The format of these results will differ depending on the result type. When successfully resolving a URL, the results will always be in the form of a dictionary.

Further documentation on the structure of these dictionaries for each result type, can be found in structures.md.

### Task.captcha

If solving a CAPTCHA is required (as indicated by the `need_captcha` state), this variable will hold a Captcha object. The Captcha class is documented further down this document.

### Task.cookiejar

The cookielib Cookie Jar that is used for this task.

### Task.run()

*Returns:* An instance of a Task-derived class, usually itself.

Runs the task.

### Task.fetch_page(url)

*Returns:* A string containing the resulting data.

Does a GET request to the specified `url`, using the Cookie Jar for the task. When manually making GET requests related to a task, always use this function to ensure that session information is retained.

### Task.post_page(url, data)

*Returns:* A string containing the resulting data.

Does a POST request to the specified `url`, using the Cookie Jar for the task. The `data` argument should be a dictionary of POST fields. When manually making POST requests related to a task, always use this function to ensure that session information is retained.

### Task.verify_password(password)

*Returns:* An instance of a Task-derived class, usually itself.

Continues the task, using the provided password. Essentially works the same as the run() method. Password validity is checked via the `state` variable. This function is only available for resolvers that support password-protected URLs.

### Task.verify_image_captcha(solution)

*Returns:* An instance of a Task-derived class, usually itself.

Continues the task, using the provided image CAPTCHA solution. Essentially works the same as the run() method. CAPTCHA solution validity is checked via the `state` variable. This function is only available for resolvers that support CAPTCHA handling.

### Task.verify_audio_captcha(solution)

*Returns:* An instance of a Task-derived class, usually itself.

Continues the task, using the provided audio CAPTCHA solution. Essentially works the same as the run() method. CAPTCHA solution validity is checked via the `state` variable. This function is only available for resolvers that support CAPTCHA handling.

### Task.verify_text_captcha(solution)

*Returns:* An instance of a Task-derived class, usually itself.

Continues the task, using the provided text CAPTCHA solution. Essentially works the same as the run() method. CAPTCHA solution validity is checked via the `state` variable. This function is only available for resolvers that support CAPTCHA handling.

## CAPTCHA handling

If a site requires a CAPTCHA to be solved before you can fully resolve the URL, the state will be set to `need_captcha`. The resolv library does not process CAPTCHAs itself; it simply provides you with the CAPTCHA data so that you can figure out some way to solve it. The `Task.captcha` variable will hold a Captcha object that has everything you will need. To provide a solution for a CAPTCHA, use the appropriate method in the Task instance (see above).

### Captcha.task

This variable will hold a reference to the `Task` this CAPTCHA belongs to.

### Captcha.text

This variable will either be `None` (if no text version of the CAPTCHA was available) or the text challenge as a string.

### Captcha.image

This variable holds `None` or the URL for the image CAPTCHA. __Do NOT use this variable unless you know what you're doing - the majority of image CAPTCHAs are tied to an IP address and set of cookies. You should use the get_image() method for this.__

### Captcha.audio

This variable holds `None` or the URL for the audio CAPTCHA. __Do NOT use this variable unless you know what you're doing - the majority of audio CAPTCHAs are tied to an IP address and set of cookies. You should use the get_audio() method for this.__

### Captcha.get_image()

*Returns:* a tuple containing (file type, binary image data).

You can save the output of this method to a file, or send it elsewhere, to further process the image CAPTCHA.

### Captcha.get_audio()

*Returns:* a tuple containing (file type, binary audio data).

You can save the output of this method to a file, or send it elsewhere, to further process the audio CAPTCHA.

### Some ideas for terminal-based CAPTCHA solving

When writing a terminal-based download application, you often can't just display a CAPTCHA to the end user. A few suggestions to work around this:

* Use a third-party CAPTCHA solving service to cover whatever CAPTCHAs can be covered.
* Implement a web interface for the application in its entirety.
* Convert the image CAPTCHA to colored text (the ASCII art approach) to display it on a terminal.
* Start a temporary HTTP daemon that serves the CAPTCHA and terminates when the CAPTCHA has been solved.

## Resolver-specific documentation

### YouTube

The YouTube resolver provides some specific custom keys for each video result: `itag` (a format identifier used by YouTube internally), `fallback_host`, and a YouTube-supplied `mimetype` definition containing encoding details.

## Documentation specific to plugin (resolver) developers

### Getting started

1. Clone the repository.
2. Look at existing resolvers, especially dummy.py to see the basic format for a resolver.
3. Modify a resolver or make your own.
4. Create a pull request to have your changes merged into the main repository (if you want to).

### Things to keep in mind

* ResolverError exceptions must always contain a user-friendly description.
* TechnicalError exceptions do not have to be user-friendly, but they must be clear.
* Don't forget to set metadata in your resolver class!
* Adhere to the standard formats for results - if you want to return something for which no suitable format exists, change the documentation to add your format and make a pull request to have it added in - this way you can be sure that applications can handle your format in the future.
* For the sake of consistency, all code, comments, and error messages should be in English.
* Always set the state of a Task to `failed`, `unsupported` or `invalid` depending on the problem, before raising an exception.
* When specifying a HTTP method, always use *uppercase* characters (GET, POST).

### Whether to use the failed, unsupported or invalid state

The `invalid` state is intended for situations where it is *certain* that the input (URL) was invalid. For example, the homepage of a filehost instead of a URL to a certain file, or an entirely different site altogether. If the URL is malformed in some way, you may also use this state. If you cannot be entirely sure whether the URL is invalid or whether there was another problem, use the `failed` state. An example of this would be a 'not authorized' page - the URL may be invalid, but it may also be possible that there is simply no public access.

The `unsupported` state is intended for situation where the URL that is provided cannot be resolved because a certain feature needed for this is not available. Examples include a CAPTCHA on a site for which the resolver has no CAPTCHA handling, or a file download on a site for which the resolver only supports resolving video streams. Use of this state should always be temporary - at some point the required functionality should be implemented.

The `failed` state is for everything else.