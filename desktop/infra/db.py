import sqlite3

from app.config import DB_FILE


def get_connection() -> sqlite3.Connection:
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if missing. Simple single-file migration for MVP."""
    schema = (
        """
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL UNIQUE,
			email TEXT NOT NULL UNIQUE,
			password_hash TEXT NOT NULL,
			created_at TEXT DEFAULT CURRENT_TIMESTAMP
		);
		"""
        """
		CREATE TABLE IF NOT EXISTS circles (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			interest TEXT NOT NULL,
			description TEXT NOT NULL,
			creator_id INTEGER NOT NULL REFERENCES users(id),
			created_at TEXT DEFAULT CURRENT_TIMESTAMP
		);
		"""
        """
		CREATE TABLE IF NOT EXISTS memberships (
			user_id INTEGER NOT NULL REFERENCES users(id),
			circle_id INTEGER NOT NULL REFERENCES circles(id),
			role TEXT NOT NULL DEFAULT 'member',
			joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (user_id, circle_id)
		);
		"""
    )
    with get_connection() as conn:
        conn.executescript(schema)
