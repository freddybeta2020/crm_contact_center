import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT DEFAULT 'agente'")
    print("Columna 'rol' agregada correctamente ✅")
except:
    print("La columna ya existe o hubo un error ⚠️")

conn.commit()
conn.close()