from database import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, title, source FROM articles")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
print(f"\nTotal articles: {len(rows)}")