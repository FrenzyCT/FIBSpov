import os
import sqlite3
import psycopg2


def get_db():
    db_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE,
            is_admin BOOLEAN DEFAULT FALSE
        );
   """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counts (
        id SERIAL PRIMARY KEY,
        name TEXT,
        value INTEGER,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );
""")

    conn.commit()
    conn.close()

