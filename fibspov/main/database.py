import sqlite3
import os
import psycopg2


def get_db():
    db_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT UNIQUE,
              VALUE INTEGER
        )
   """)
    cursor.execute("INSERT OR IGNORE INTO counts (name, value) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING", ('phone', 0))
    cursor.execute("INSERT OR IGNORE INTO counts (name, value) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING", ('direct', 0))
    conn.commit()
    conn.close()

