import sqlite3

DB = "database/pentest.db"


def create_engagement(target, objective):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO engagements
        (target, objective, status)
        VALUES (?, ?, ?)
        """,
        (target, objective, "active")
    )

    conn.commit()
    conn.close()


def get_active_engagement():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id,target,objective
        FROM engagements
        WHERE status='active'
        ORDER BY id DESC
        LIMIT 1
        """
    )

    result = cur.fetchone()

    conn.close()

    return result
