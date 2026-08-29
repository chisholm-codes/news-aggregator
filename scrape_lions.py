import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timedelta
import time

LISTING_URL = "https://www.detroitlions.com/news/the-daily-drive"
HEADERS = {"User-Agent": "Mozilla/5.0"}
SOURCE_NAME = "Detroit Lions"


def get_article_links():
    """Scrape the listing page for article (title, url) pairs, newest first."""
    response = requests.get(LISTING_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    seen = set()
    for link in soup.find_all("a", href=True):
        text = link.get_text(strip=True)
        if not text.startswith("news"):
            continue
        full_url = urljoin(LISTING_URL, link["href"])
        if full_url in seen:
            continue
        seen.add(full_url)
        articles.append((text[len("news"):], full_url))
    return articles


def get_article_date(article_url):
    """Fetch an individual article page and return its publish date, or None."""
    response = requests.get(article_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    date_div = soup.find("div", class_="nfl-c-article__dates")
    if not date_div:
        return None

    date_text = date_div.get_text(strip=True)
    try:
        return datetime.strptime(date_text, "%b %d, %Y at %I:%M %p")
    except ValueError:
        return None


def scrape_lions():
    """Scrape Detroit Lions articles from the last 7 days into the articles table."""
    from fetch_feeds import save_article

    cutoff = datetime.now() - timedelta(days=7)
    count = 0

    for title, link in get_article_links():
        published = get_article_date(link)
        time.sleep(1)

        if published is None:
            continue
        if published < cutoff:
            break

        save_article(title, link, SOURCE_NAME, published.strftime("%Y-%m-%d %H:%M:%S"))
        count += 1

    print(f"Lions scrape complete. Saved/updated {count} articles from the last 7 days.")


if __name__ == "__main__":
    scrape_lions()