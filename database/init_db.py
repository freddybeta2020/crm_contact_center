import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "crm.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    email TEXT UNIQUE
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    rol TEXT DEFAULT 'agente'
)
""")

# Insertamos el admin solo si no existe aún (evita error por email duplicado)
admin_existe = cursor.execute(
    "SELECT id FROM usuarios WHERE email = ?", ("admin@test.com",)
).fetchone()

if not admin_existe:
    password_hash = generate_password_hash("1234")
    conn.execute(
        "INSERT INTO usuarios (email, password, rol) VALUES (?, ?, ?)",
        ("admin@test.com", password_hash, "admin")
    )
    conn.commit()
    print("Admin creado correctamente 🔥")
else:
    print("El admin ya existe, no se insertó de nuevo.")



# ─────────────────────────────────────────────
# TABLA: llamadas
# ─────────────────────────────────────────────
# Esta tabla guarda cada interacción que un agente
# tuvo con un cliente. Es el corazón del Contact Center.
#
# Relaciones:
#   - cliente_id → apunta a clientes.id  (a quién se llamó)
#   - usuario_id → apunta a usuarios.id  (quién hizo la llamada)
#
# FOREIGN KEY le dice a SQLite que esos ids deben
# existir en sus tablas correspondientes — no puedes
# registrar una llamada a un cliente que no existe.
# ─────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS llamadas (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id  INTEGER NOT NULL,
    usuario_id  INTEGER NOT NULL,
    fecha       TEXT    NOT NULL,
    resultado   TEXT    NOT NULL,
    notas       TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
""")

conn.commit()
print("Tabla llamadas lista ✅")

print("Base de datos lista ✅")

conn.close()