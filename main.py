from fastapi import FastAPI
from database import get_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "News aggregator API is running"}

@app.get("/articles")
def get_articles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, link, source, published FROM articles ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    articles = []
    for row in rows:
        articles.append({
            "id": row[0],
            "title": row[1],
            "link": row[2],
            "source": row[3],
            "published": row[4],
        })

    return articles