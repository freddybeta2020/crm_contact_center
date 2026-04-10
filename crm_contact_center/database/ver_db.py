import sqlite3

conn = sqlite3.connect("database/crm.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(usuarios)")
columnas = cursor.fetchall()

for col in columnas:
    print(col)

conn.close()