## URLs

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>url</td>
		<td>The deobfuscated or un-shortened URL.</td>
	</tr>
</table>

## Dummy data

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>dummy</td>
		<td>The dummy data.</td>
	</tr>
</table>

## Video

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>title</td>
		<td>Title of the video.</td>
	</tr>
	<tr>
		<td>videos</td>
		<td>A list of all available video files.</td>
	</tr>
</table>

The list of videos can contain multiple dictionaries, each of which has the following fields:

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>url</td>
		<td>URL of the video file.</td>
	</tr>
	<tr>
		<td>method</td>
		<td>The method to be used for retrieving this URL (either GET or POST).</td>
	</tr>
	<tr>
		<td>postdata</td>
		<td>(optional) The POST data to send if the method to be used is POST. This data is in dictionary form.</td>
	</tr>
	<tr>
		<td>quality</td>
		<td>A textual description of the video quality (this will typically be along the lines of `360p`, `720p`, `1080p`, `low`, `medium`, `high`, etc, but any value 
			is possible). If the quality is not specified, this will be set to `unknown`. Don't parse this programmatically - use the `priority` field instead.</td>
	</tr>
	<tr>
		<td>format</td>
		<td>The name of the file format for this video, along the lines of `webm`, `mp4`, `3gp`, `flv`, `wmv`, etc. While this value should typically be pretty consistent,
			different abbreviations may be used for different resolvers. It's probably not a good idea to automatically parse these unless you know the exact values
			a resolver will return. This may be set to `unknown`.</td>
	</tr>
	<tr>
		<td>priority</td>
		<td>The priority for this video file. Higher quality video has a lower 'priority'. To always get the highest quality video, go for the URL with the lowest
			priority (this may not always be 1).</td>
	</tr>
	<tr>
		<td>extra</td>
		<td>This is a dictionary that may contain any custom data provided by the specific resolver that is used. Refer to the resolver-specific documentation for this.</td>
	</tr>
</table>

## Audio

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>title</td>
		<td>Title of the audio file.</td>
	</tr>
	<tr>
		<td>audiofiles</td>
		<td>A list of all available audio files.</td>
	</tr>
</table>

The list of audio files can contain multiple dictionaries, each of which has the following fields:

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>url</td>
		<td>URL of the audio file.</td>
	</tr>
	<tr>
		<td>method</td>
		<td>The method to be used for retrieving this URL (either GET or POST).</td>
	</tr>
	<tr>
		<td>postdata</td>
		<td>(optional) The POST data to send if the method to be used is POST. This data is in dictionary form.</td>
	</tr>
	<tr>
		<td>quality</td>
		<td>A textual description of the audio quality (this will typically be along the lines of `low`, `medium`, `high`, `lossless`, etc, but any value is possible). If 
		the quality is not specified, this will be set to `unknown`. Don't parse this programmatically - use the `priority` field instead.</td>
	</tr>
	<tr>
		<td>format</td>
		<td>The name of the file format for this audio file, along the lines of `mp3`, `flac`, `midi`, `ogg`, etc. While this value should typically be pretty consistent,
			different abbreviations may be used for different resolvers. It's probably not a good idea to automatically parse these unless you know the exact values
			a resolver will return. This may be set to `unknown`.</td>
	</tr>
	<tr>
		<td>priority</td>
		<td>The priority for this audio file. Higher quality audio has a lower 'priority'. To always get the highest quality audio file, go for the URL with the lowest
			priority (this may not always be 1).</td>
	</tr>
	<tr>
		<td>extra</td>
		<td>This is a dictionary that may contain any custom data provided by the specific resolver that is used. Refer to the resolver-specific documentation for this.</td>
	</tr>
</table>

## Images

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>title</td>
		<td>Title of the image.</td>
	</tr>
	<tr>
		<td>images</td>
		<td>A list of all available image files.</td>
	</tr>
</table>

The list of images can contain multiple dictionaries, each of which has the following fields:

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>url</td>
		<td>URL of the image.</td>
	</tr>
	<tr>
		<td>method</td>
		<td>The method to be used for retrieving this URL (either GET or POST).</td>
	</tr>
	<tr>
		<td>postdata</td>
		<td>(optional) The POST data to send if the method to be used is POST. This data is in dictionary form.</td>
	</tr>
	<tr>
		<td>quality</td>
		<td>A textual description of the image quality (this will typically be along the lines of `low`, `medium`, `high`, `lossless`, etc, but any value is possible). If 
		the quality is not specified, this will be set to `unknown`. Don't parse this programmatically - use the `priority` field instead.</td>
	</tr>
	<tr>
		<td>format</td>
		<td>The name of the file format for this image, along the lines of `jpg`, `png`, `psd`, `svg`, etc. While this value should typically be pretty consistent,
			different abbreviations may be used for different resolvers. It's probably not a good idea to automatically parse these unless you know the exact values
			a resolver will return. This may be set to `unknown`.</td>
	</tr>
	<tr>
		<td>priority</td>
		<td>The priority for this image. Higher quality images have a lower 'priority'. To always get the highest quality image, go for the URL with the lowest
			priority (this may not always be 1).</td>
	</tr>
	<tr>
		<td>extra</td>
		<td>This is a dictionary that may contain any custom data provided by the specific resolver that is used. Refer to the resolver-specific documentation for this.</td>
	</tr>
</table>

## Files

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>title</td>
		<td>Title of the file.</td>
	</tr>
	<tr>
		<td>files</td>
		<td>A list of all available URLs for this file.</td>
	</tr>
</table>

The list of files can contain multiple dictionaries, each of which has the following fields:

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>url</td>
		<td>URL of the file.</td>
	</tr>
	<tr>
		<td>method</td>
		<td>The method to be used for retrieving this URL (either GET or POST).</td>
	</tr>
	<tr>
		<td>postdata</td>
		<td>(optional) The POST data to send if the method to be used is POST. This data is in dictionary form.</td>
	</tr>
	<tr>
		<td>format</td>
		<td>The name of the file format, along the lines of `zip`, `mp3`, `pdf`, `doc`, etc. While this value should typically be pretty consistent,
			different abbreviations may be used for different resolvers. It's probably not a good idea to automatically parse these unless you know the exact values
			a resolver will return. This may be set to `unknown`.</td>
	</tr>
	<tr>
		<td>priority</td>
		<td>The priority for this URL. More important or faster URLs have a lower 'priority'. To always get the best result, go for the URL with the lowest
			priority (this may not always be 1).</td>
	</tr>
	<tr>
		<td>extra</td>
		<td>This is a dictionary that may contain any custom data provided by the specific resolver that is used. Refer to the resolver-specific documentation for this.</td>
	</tr>
</table>

## Text

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>title</td>
		<td>Title of the text file.</td>
	</tr>
	<tr>
		<td>files</td>
		<td>A list of all available URLs for this file.</td>
	</tr>
</table>

The list of text files can contain multiple dictionaries, each of which has the following fields:

<table>
	<tr>
		<th>Key</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>url</td>
		<td>URL of the file.</td>
	</tr>
	<tr>
		<td>method</td>
		<td>The method to be used for retrieving this URL (either GET or POST).</td>
	</tr>
	<tr>
		<td>postdata</td>
		<td>(optional) The POST data to send if the method to be used is POST. This data is in dictionary form.</td>
	</tr>
	<tr>
		<td>format</td>
		<td>The name of the file format, along the lines of `zip`, `mp3`, `pdf`, `doc`, etc. While this value should typically be pretty consistent,
			different abbreviations may be used for different resolvers. It's probably not a good idea to automatically parse these unless you know the exact values
			a resolver will return. This may be set to `unknown`.</td>
	</tr>
	<tr>
		<td>priority</td>
		<td>The priority for this URL. More important or faster URLs have a lower 'priority'. To always get the best result, go for the URL with the lowest
			priority (this may not always be 1).</td>
	</tr>
	<tr>
		<td>extra</td>
		<td>This is a dictionary that may contain any custom data provided by the specific resolver that is used. Refer to the resolver-specific documentation for this.</td>
	</tr>
</table>