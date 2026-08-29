import feedparser
import time
from database import get_connection, create_table
from datetime import datetime, timedelta

def save_article(title, link, source, published):
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO articles (title, link, source, published)
            VALUES (?, ?, ?, ?)
        """, (title, link, source, published))
        conn.commit()
    except ValueError:
        # This link already exists in the database — skip it
        pass

def get_sources():
    conn = get_connection()
    sources = conn.execute("SELECT name, url FROM sources").fetchall()
    return sources

def fetch_all():
    create_table()
    sources = get_sources()
    delete_old_articles()
    cutoff = datetime.now() - timedelta(days=7)

    for name, url in sources:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published_date = ""
            entry_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_date = time.strftime("%Y-%m-%d %H:%M:%S", entry.published_parsed)
                entry_date = datetime(*entry.published_parsed[:6]) 

            if entry_date is None or entry_date > cutoff:
                save_article(
                    entry.title,
                    entry.link,
                    name,
                    published_date,
                )
    try:
        from scrape_lions import scrape_lions
        scrape_lions()
    except Exception as e:
        print(f"Lions scrape failed: {e}")

    print("Fetch complete.")
    

def delete_old_articles():
    conn = get_connection()
    cutoff = datetime.now() - timedelta(days=7)
    cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M:%S")

    conn.execute("DELETE FROM articles WHERE published < ?", (cutoff_str,))
    conn.commit()

if __name__ == "__main__":
    fetch_all()