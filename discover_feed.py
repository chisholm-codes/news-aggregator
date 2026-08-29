import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import feedparser

HEADERS = {"User-Agent": "Mozilla/5.0"}
FEED_TYPES = ["application/rss+xml", "application/atom+xml", "application/feed+json"]


def discover_feed(url):
    """Given a site or feed URL, return a usable feed URL, or None if none found."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException:
        return None

    # Is the URL already a feed?
    if feedparser.parse(response.content).entries:
        return url

    # Otherwise scan the page's <head> for feed autodiscovery <link> tags
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("link", rel="alternate"):
        if link.get("type") in FEED_TYPES and link.get("href"):
            candidate = urljoin(url, link["href"])
            if feedparser.parse(candidate).entries:
                return candidate

    return None


if __name__ == "__main__":
    import sys
    print(discover_feed(sys.argv[1]))