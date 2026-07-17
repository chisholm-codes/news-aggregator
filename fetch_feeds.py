import feedparser

urls =  [
    "https://hnrss.org/frontpage",
    "https://feeds.arstechnica.com/arstechnica/index",
]

for url in urls:
    feed = feedparser.parse(url)
    print (f"--- {feed.feed.get('title', url)} ---")
    for entry in feed.entries:
        print(entry.title)
    print()
