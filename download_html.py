import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError

def Download(url, num_retries=2):
	print('Downloading:', url)
	try:
		html = urllib.request.urlopen(url).read()
	except(URLError, HTTPError, ContentTooShortError) as e:
		print('Downloading error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				# recursively retry 5xx HTTP errors
				return Download(url, num_retries - 1)
	return html


if __name__ == '__main__':
	Download('http://httpstat.us/500')
