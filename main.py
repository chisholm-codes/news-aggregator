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
    query += " ORDER BY published DESC"

    rows = conn.execute(query, params).fetchall()

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

@app.post("/fetch")
def trigger_fetch():
    fetch_all()
    return {"status": "fetch complete"}

@app.get("/sources")
def get_sources():
    conn = get_connection()
    rows = conn.execute("SELECT id, name, url FROM sources").fetchall()
    return [{"id": row[0], "name": row[1], "url": row[2]} for row in rows]

@app.post("/sources")
def add_source(name: str, url: str):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO sources (name, url) VALUES (?, ?)", (name, url))
        conn.commit()
    except ValueError:
        return {"error": "That URL is already added."}
    return {"status": "added", "name": name, "url": url}

@app.delete("/sources/{source_id}")
def delete_source(source_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM sources WHERE id = ?", (source_id,))
    conn.commit()
    return {"status": "deleted", "id": source_id}