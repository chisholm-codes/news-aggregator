# News Aggregator

A personal news aggregator that pulls RSS feeds and email newsletters into a single daily reading feed. Built as a learning project — designed to feel like a feed to scroll, not an inbox to manage.

Live app: https://news-aggregator-9fta.onrender.com

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** [Turso](https://turso.tech) (hosted libSQL, SQLite-compatible)
- **Scheduling:** APScheduler — fetches feeds on startup and every 24 hours
- **Frontend:** Plain HTML/CSS/JS
- **Hosting:** [Render](https://render.com)

## External Service Dependencies

This app depends on two external services to run:

### Render
Hosts the FastAPI app and handles deployment. Auto-deploys on every push to `main`.

### Turso
Hosted SQLite-compatible database used for storing articles and sources. Turso was chosen after discovering that Render's free-tier disk is ephemeral — a local SQLite file would get wiped on every restart or spin-down, losing all saved data.

Required environment variables (set in Render's dashboard, and locally in a `.env` file — never committed to Git):
- `TURSO_DATABASE_URL`
- `TURSO_AUTH_TOKEN`

## Local Development

1. Clone the repo and create a virtual environment
2. `pip install -r requirements.txt`
3. Create a `.env` file in the project root with your own Turso credentials:
   ```
   TURSO_DATABASE_URL=your-url-here
   TURSO_AUTH_TOKEN=your-token-here
   ```
4. Run the app:
   ```
   uvicorn main:app --reload
   ```
5. Visit `http://127.0.0.1:8000`

## Features

- Pulls articles from RSS feeds and email newsletters (via [Kill the Newsletter](https://kill-the-newsletter.com/))
- Manual refresh button, plus automatic daily fetching
- Add/remove sources directly from the UI
- Deduplicates articles automatically
