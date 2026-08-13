import feedparser
import time
from database import get_connection, create_table

def save_article(conn, title, link, source, published):
    try:
        conn.execute("""
            INSERT INTO articles (title, link, source, published)
            VALUES (?, ?, ?, ?)
        """, (title, link, source, published))
    except ValueError:
        # This link already exists in the database — skip it
        pass

def get_sources():
    conn = get_connection()
    sources = conn.execute("SELECT name, url FROM sources").fetchall()
    return sources

def fetch_all():
    create_table()
    conn = get_connection()

    sources = get_sources()

    for name, url in sources:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published_date = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_date = time.strftime("%Y-%m-%d %H:%M:%S", entry.published_parsed)

            save_article(
                conn,
                entry.title,
                entry.link,
                name,
                published_date,
            )

    conn.commit()
    print("Fetch complete.")

if __name__ == "__main__":
    fetch_all()