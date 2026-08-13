from database import get_connection, create_table

sources = [
    ("Hacker News", "https://hnrss.org/frontpage"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("The Skimm", "https://kill-the-newsletter.com/feeds/yy4thlgfugnxqlrul4wp.xml"),
    ("San Pedro Gazette", "https://kill-the-newsletter.com/feeds/wbiiuj15clqojigfiaps.xml"),
    ("TLDR", "https://kill-the-newsletter.com/feeds/0k9t5zcjbg7h1hvqz709.xml"),
]

def seed():
    create_table()
    conn = get_connection()
    cursor = conn.cursor()
    for name, url in sources:
        try:
            cursor.execute("INSERT INTO sources (name, url) VALUES (?, ?)", (name, url))
        except Exception as e:
            print(f"Skipped {name}: {e}")
    conn.commit()
    conn.close()
    print("Sources seeded.")

if __name__ == "__main__":
    seed()