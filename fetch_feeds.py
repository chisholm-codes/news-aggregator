import feedparser
import sqlite3
from database import get_connection, create_table

urls = [
    "https://hnrss.org/frontpage",
    "https://feeds.arstechnica.com/arstechnica/index",
]

def save_article(cursor, title, link, source, published):
    try:
        cursor.execute("""
            INSERT INTO articles (title, link, source, published)
            VALUES (?, ?, ?, ?)
        """, (title, link, source, published))
    except sqlite3.IntegrityError:
        # This link already exists in the database — skip it
        pass

def fetch_all():
    create_table()
    conn = get_connection()
    cursor = conn.cursor()

    for url in urls:
        feed = feedparser.parse(url)
        source_name = feed.feed.get("title", url)
        for entry in feed.entries:
            save_article(
                cursor,
                entry.title,
                entry.link,
                source_name,
                entry.get("published", ""),
            )

    conn.commit()
    conn.close()
    print("Fetch complete.")

if __name__ == "__main__":
    fetch_all()
