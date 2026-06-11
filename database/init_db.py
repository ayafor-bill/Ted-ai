import sqlite3

conn = sqlite3.connect("database/pentest.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS engagements (
    id INTEGER PRIMARY KEY,
    target TEXT,
    objective TEXT,
    status TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS findings (
    id INTEGER PRIMARY KEY,
    engagement_id INTEGER,
    finding TEXT,
    confidence REAL
)
""")

conn.commit()
conn.close()

print("Database initialized")
