import re
import urllib.request
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError, ContentTooShortError


def download(url, num_retries=2, user_agent='wswp', charset='utf-8'):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html

def get_links(html):
    """ Return a list of links from html : A regular expression to extrace all links from the webpages """
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list all links from webpage
    return webpage_regex.findall(html)


def link_crawler(start_url, link_regex):
    """ Crawl from the given start URL following links matched by link_regex """
    crawl_queue = [start_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        if not html:
            continue
        # filter for links matching our regular expression
        for link in get_links(html):
            #print(link)
            if re.match(link_regex, link):
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    seen.add(abs_link)
                    crawl_queue.append(abs_link)

if __name__ == '__main__':
    link_crawler('http://example.python-scraping.com', '(/places/default/index/|/places/default/view/)')