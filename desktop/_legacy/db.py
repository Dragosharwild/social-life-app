# db.py
import sqlite3

DB_FILE = "circlesync.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def user_exists(username: str, email: str) -> tuple[bool, bool]:
    """Return (username_taken, email_taken)."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT 1 FROM accounts WHERE lower(username)=lower(?) LIMIT 1", (username,))
    u = c.fetchone() is not None
    c.execute("SELECT 1 FROM accounts WHERE lower(email)=lower(?) LIMIT 1", (email,))
    e = c.fetchone() is not None
    conn.close()
    return u, e

def create_user(email: str, username: str, password: str) -> tuple[bool, str | None]:
    email, username = email.strip(), username.strip()

    username_taken, email_taken = user_exists(username, email)
    if username_taken and email_taken:
        return False, "That username and email are already taken."
    if username_taken:
        return False, "That username is already taken."
    if email_taken:
        return False, "That email is already taken."

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO accounts (email, username, password)
            VALUES (?, ?, ?)
        """, (email, username, password))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        # Fallback in case of race conditions
        msg = str(e).lower()
        if "username" in msg:
            return False, "That username is already taken."
        if "email" in msg:
            return False, "That email is already taken."
        return False, "That username or email is already taken."
    finally:
        conn.close()

def authenticate(identifier: str, password: str) -> bool:
    identifier = identifier.strip()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT password
        FROM accounts
        WHERE lower(username)=lower(?) OR lower(email)=lower(?)
        LIMIT 1
    """, (identifier, identifier))
    row = c.fetchone()
    conn.close()
    return bool(row) and row[0] == password
