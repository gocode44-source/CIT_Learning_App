import sqlite3

DB_NAME = "data/progress.db"

def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_table():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY,
        username TEXT,
        chapter TEXT,
        xp INTEGER
    )
    """)

    conn.commit()
    conn.close()

def complete_chapter(username, chapter, xp):
    conn = connect()
    c = conn.cursor()

    c.execute("INSERT INTO progress (username, chapter, xp) VALUES (?, ?, ?)",
              (username, chapter, xp))

    conn.commit()
    conn.close()

def get_progress(username):
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT * FROM progress WHERE username=?", (username,))
    data = c.fetchall()

    conn.close()
    return data
