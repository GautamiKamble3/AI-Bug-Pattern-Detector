import sqlite3
from datetime import datetime

DB_NAME = "bugs.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bug_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            filename TEXT,
            bugs TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()



def save_bug_report(username, filename, bugs):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    bug_text = ", ".join(bugs) if bugs else "No bugs"

    cursor.execute("""
        INSERT INTO bug_reports (username, filename, bugs, timestamp)
        VALUES (?, ?, ?, ?)
    """, (username, filename, bug_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()



def get_all_reports(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT filename, bugs, timestamp
        FROM bug_reports
        WHERE username = ?
        ORDER BY id DESC
    """, (username,))

    reports = cursor.fetchall()
    conn.close()
    return reports



# -------- USERS --------

def init_user_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def validate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    conn.close()
    return user is not None
