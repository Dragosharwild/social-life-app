import sqlite3

DB_FILE = "circlesync.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print("-", table[0])

conn.close()