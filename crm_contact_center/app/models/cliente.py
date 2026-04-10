from app.models.user import get_db_connection           

def crear_cliente(nombre, telefono, email):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO clientes (nombre, telefono, email) VALUES (?, ?, ?)",
        (nombre, telefono, email)
    )
    conn.commit()
    conn.close()
    
def obtener_clientes():
    conn = get_db_connection()
    clientes = conn.execute("SELECT * FROM clientes").fetchall()
    conn.close()
    return clientes
    
    
def eliminar_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()    
    
def contar_clientes():
    conn = get_db_connection()
    total = conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    conn.close()
    return total

def buscar_clientes(termino):
    """
    Busca coincidencias en nombre o teléfono.
    El símbolo % permite que busque el texto en cualquier parte de la palabra.
    """
    conn = get_db_connection()
    # Usamos LIKE para que coincida aunque no escriban el nombre completo
    query = "SELECT * FROM clientes WHERE nombre LIKE ? OR telefono LIKE ?"
    
    # Preparamos el término: 'Fredy' -> '%Fredy%'
    filtro = f"%{termino}%"
    
    clientes = conn.execute(query, (filtro, filtro)).fetchall()
    conn.close()
    return clientes

def obtener_cliente_por_id(cliente_id):
    """Busca los datos de un solo cliente para cargarlos en el formulario."""
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
    conn.close()
    return cliente

def actualizar_cliente(cliente_id, nombre, telefono, email):
    """Guarda los cambios realizados en el perfil del cliente."""
    conn = get_db_connection()
    conn.execute(
        "UPDATE clientes SET nombre = ?, telefono = ?, email = ? WHERE id = ?",
        (nombre, telefono, email, cliente_id)
    )
    conn.commit()
    conn.close()
