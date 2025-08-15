import sqlite3

conn = sqlite3.connect("circlesync.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS accounts")  # Deletes the users table
conn.commit()
conn.close()

print("Table deleted.")