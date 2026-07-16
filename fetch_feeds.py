import feedparser

url = "https://hnrss.org/frontpage"
feed = feedparser.parse(url)

for entry in feed.entries:
    print(entry.title)