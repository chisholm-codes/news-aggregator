import feedparser
import sqlite3
import time
from database import get_connection, create_table

def save_article(cursor, title, link, source, published):
    try:
        cursor.execute("""
            INSERT INTO articles (title, link, source, published)
            VALUES (?, ?, ?, ?)
        """, (title, link, source, published))
    except sqlite3.IntegrityError:
        # This link already exists in the database — skip it
        pass

def get_sources():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, url FROM sources")
    sources = cursor.fetchall()
    conn.close()
    return sources

def fetch_all():
    create_table()
    conn = get_connection()
    cursor = conn.cursor()

    sources = get_sources()

    for name, url in sources:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published_date = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_date = time.strftime("%Y-%m-%d %H:%M:%S", entry.published_parsed)

            save_article(
                cursor,
                entry.title,
                entry.link,
                name,
                published_date,
            )

    conn.commit()
    conn.close()
    print("Fetch complete.")

if __name__ == "__main__":
    fetch_all()