import sqlite3
import datetime

DB_NAME = "data/progress.db"

def create_streak_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS streak (
        id INTEGER PRIMARY KEY,
        username TEXT,
        last_date TEXT,
        streak_count INTEGER
    )
    """)

    conn.commit()
    conn.close()

def update_streak(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    today = str(datetime.date.today())

    c.execute("SELECT last_date, streak_count FROM streak WHERE username=?", (username,))
    row = c.fetchone()

    if row:
        last_date, count = row
        if last_date != today:
            count += 1
        c.execute("UPDATE streak SET last_date=?, streak_count=? WHERE username=?",
                  (today, count, username))
    else:
        c.execute("INSERT INTO streak (username, last_date, streak_count) VALUES (?, ?, ?)",
                  (username, today, 1))

    conn.commit()
    conn.close()

def get_streak(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT streak_count FROM streak WHERE username=?", (username,))
    row = c.fetchone()

    conn.close()
    return row[0] if row else 0
