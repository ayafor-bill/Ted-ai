"""Simple database initialization - bypass complex schema"""

import sqlite3
from pathlib import Path

def init_database():
    """Initialize fresh database with simple schema"""
    db_path = "ted_ai.db"
    
    # Remove old database and all related files
    for f in [db_path, f"{db_path}-journal", f"{db_path}-wal", f"{db_path}-shm"]:
        if Path(f).exists():
            Path(f).unlink()
    
    # Create database
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    
    # Create basic tables (without complex indexes)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS engagements (
            id INTEGER PRIMARY KEY,
            target_name TEXT UNIQUE NOT NULL,
            target_type TEXT NOT NULL,
            status TEXT DEFAULT 'planning',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    
    print(f"✓ Database initialized at {db_path}")

if __name__ == "__main__":
    init_database()