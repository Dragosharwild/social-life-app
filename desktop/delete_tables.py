import sqlite3

conn = sqlite3.connect("accounts.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")  # Deletes the users table
cursor.execute("DROP TABLE IF EXISTS interests")
cursor.execute("DROP TABLE IF EXISTS bubbles")
conn.commit()
conn.close()

print("Table deleted.")