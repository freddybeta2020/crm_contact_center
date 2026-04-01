import sqlite3
import os
# Importamos herramientas para encriptar contraseñas (Seguridad profesional)
from werkzeug.security import generate_password_hash, check_password_hash
from database.init_db import DB_PATH

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
# Función para crear un nuevo usuario
def crear_usuario(email, password):
    conn = get_db_connection()

    password_hash = generate_password_hash(password)

    conn.execute(
        "INSERT INTO usuarios (email, password) VALUES (?, ?)",
        (email, password_hash)
    )

    conn.commit()
    conn.close()
# Función para buscar un usuario por email y contraseña
def buscar_usuario(email, password):
    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM usuarios WHERE email = ?",
        (email,)
    ).fetchone()

    conn.close()

    print("USUARIO ENCONTRADO:", user)
# Verificamos la contraseña usando check_password_hash
    if user and check_password_hash(user["password"], password):
     return user

    return None