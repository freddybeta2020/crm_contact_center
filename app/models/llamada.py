# ─────────────────────────────────────────────────────────
# MODELO: llamada.py
# ─────────────────────────────────────────────────────────
# Este archivo maneja toda la comunicación entre Python
# y la tabla "llamadas" de la base de datos.
#
# Patrón que seguimos: cada función hace UNA sola cosa.
# Eso se llama "responsabilidad única" y hace que el
# código sea más fácil de leer, probar y mantener.
# ─────────────────────────────────────────────────────────

from app.models.user import get_db_connection
from datetime import datetime


def registrar_llamada(cliente_id, usuario_email, resultado, notas):
    """
    Guarda una nueva llamada en la base de datos.

    Parámetros:
        cliente_id    → id del cliente al que se llamó
        usuario_email → email del agente (lo tenemos en session["usuario"])
        resultado     → qué pasó en la llamada (contestó, no contestó, etc.)
        notas         → comentarios adicionales del agente (puede ser vacío)

    ¿Por qué guardamos usuario_email y no usuario_id?
    Porque en la sesión de Flask guardamos el email, no el id.
    Primero buscamos el id del usuario usando ese email.
    """
    conn = get_db_connection()

    # Paso 1: buscamos el id del usuario a partir de su email
    # Necesitamos el id porque la tabla llamadas guarda usuario_id (número)
    usuario = conn.execute(
        "SELECT id FROM usuarios WHERE email = ?",
        (usuario_email,)
    ).fetchone()

    # Paso 2: obtenemos la fecha y hora actual del sistema
    # strftime formatea la fecha como texto: "2026-04-09 14:35:00"
    # Así queda legible y ordenable en la base de datos
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Paso 3: insertamos el registro en la tabla llamadas
    conn.execute(
        """
        INSERT INTO llamadas (cliente_id, usuario_id, fecha, resultado, notas)
        VALUES (?, ?, ?, ?, ?)
        """,
        (cliente_id, usuario["id"], fecha_actual, resultado, notas)
    )

    conn.commit()
    conn.close()


def obtener_llamadas_de_cliente(cliente_id):
    """
    Devuelve todas las llamadas de un cliente específico.

    Usamos JOIN para combinar la tabla llamadas con usuarios,
    así podemos mostrar el email del agente en lugar de su id.

    ¿Qué es un JOIN?
    Es como unir dos tablas en una sola consulta.
    Sin JOIN tendrías que hacer dos consultas separadas.

    El resultado incluye todos los campos de llamadas
    más el email del agente que la realizó.
    """
    conn = get_db_connection()

    llamadas = conn.execute(
        """
        SELECT
            llamadas.id,
            llamadas.fecha,
            llamadas.resultado,
            llamadas.notas,
            usuarios.email AS agente
        FROM llamadas
        JOIN usuarios ON llamadas.usuario_id = usuarios.id
        WHERE llamadas.cliente_id = ?
        ORDER BY llamadas.fecha DESC
        """,
        (cliente_id,)
    ).fetchall()

    conn.close()
    return llamadas


def contar_llamadas():
    """
    Devuelve el número total de llamadas registradas.
    Lo usaremos en el dashboard para mostrar estadísticas.
    """
    conn = get_db_connection()
    total = conn.execute("SELECT COUNT(*) FROM llamadas").fetchone()[0]
    conn.close()
    return total