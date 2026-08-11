from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from apscheduler.schedulers.background import BackgroundScheduler
from database import get_connection
from fetch_feeds import fetch_all

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Running initial fetch on startup...")
    fetch_all()
    scheduler.add_job(fetch_all, "interval", hours=24)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.get("/articles")
def get_articles(unread_only: bool = False, source: str = None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, title, link, source, published, read FROM articles"
    conditions = []
    params = []

    if unread_only:
        conditions.append("read = 0")
    if source:
        conditions.append("source = ?")
        params.append(source)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY id DESC"

    cursor.execute(query, params)
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
            "read": bool(row[5]),
        })

    return articles

@app.post("/articles/{article_id}/read")
def mark_read(article_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE articles SET read = 1 WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()
    return {"id": article_id, "read": True}