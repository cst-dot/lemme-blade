import sqlite3

DB = "game.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS state (
        id INTEGER PRIMARY KEY,
        darkness REAL
    )
    """)

    c.execute("INSERT OR IGNORE INTO state (id, darkness) VALUES (1, 0.2)")

    conn.commit()
    conn.close()


def save_memory(text):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO memory (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()


def get_memory(limit=5):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT text FROM memory ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_darkness():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT darkness FROM state WHERE id=1")
    val = c.fetchone()[0]
    conn.close()
    return val


def update_darkness(val):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE state SET darkness=? WHERE id=1", (val,))
    conn.commit()
    conn.close()
