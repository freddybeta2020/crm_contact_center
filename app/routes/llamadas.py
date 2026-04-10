# ─────────────────────────────────────────────────────────
# RUTAS: llamadas.py
# ─────────────────────────────────────────────────────────
# Este archivo maneja las URLs relacionadas con llamadas.
#
# ¿Qué es un Blueprint?
# Es una forma de organizar rutas en grupos separados.
# En lugar de tener TODAS las rutas en un solo archivo
# enorme, cada módulo tiene su propio Blueprint.
# Flask los une todos cuando arranca la aplicación.

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.llamada import registrar_llamada,obtener_llamadas_de_cliente
from app.models.cliente import obtener_cliente_por_id

# Creamos el Blueprint con el nombre "llamadas"
# Ese nombre es el que usamos en url_for("llamadas.nombre_funcion")

llamadas_bp = Blueprint("llamadas", __name__)

@llamadas_bp.route("/clientes/<int:cliente_id>/llamadas")
def historial(cliente_id):
    """
    Muestra el historial completo de llamadas de un cliente.

    Recibe el id del cliente en la URL, por ejemplo:
        /clientes/5/llamadas  →  muestra las llamadas del cliente con id=5

    ¿Ves el <int:cliente_id> en la ruta?
    Flask convierte automáticamente ese fragmento de la URL
    a un número entero y lo pasa como parámetro a la función.
    """
    # Protección: si no hay sesión activa, mandamos al login
    if "usuario_id" not in session:
        return redirect(url_for("autho.login"))

    # Traemos los datos del cliente para mostrar su nombre en la página
    cliente = obtener_llamadas_de_cliente(cliente_id)

    # Traemos todas sus llamadas usando el JOIN que definimos en el modelo
    llamadas = obtener_llamadas_de_cliente(cliente_id)

    return render_template(
        "historial_llamadas.html",
        cliente=cliente,
        llamadas=llamadas
    )

@llamadas_bp.route("/clientes/<int:cliente_id>/llamadas/nueva", methods=["GET", "POST"])
def nueva_llamda(cliente_id):
    """
    GET  → muestra el formulario para registrar una llamada
    POST → recibe los datos del formulario y los guarda en la BD

    ¿Por qué una sola ruta maneja GET y POST?
    Es una convención en Flask: la misma URL sirve para
    mostrar el formulario (GET) y para procesarlo (POST).
    Así la URL queda limpia y semántica.
    """
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    # Traemos el cliente para mostrar su nombre en el formulario
    cliente = obtener_cliente_por_id(cliente_id)

    if request.method == "POST":
        # Recogemos los datos que el agente escribió en el formulario
        resultado = request.form["resultado"]
        notas = request.form.get("notas", "")
        # .get() con valor por defecto "" porque las notas son opcionales
        # Si usáramos request.form["notas"] y el campo estuviera vacío
        # Flask lanzaría un error — .get() lo evita

        # Registramos la llamada en la base de datos
        # Pasamos session["usuario"] para saber qué agente hizo la llamada
        registrar_llamada(cliente_id, session["usuario"], resultado, notas)

        flash(f"Llamada registrada correctamente para {cliente['nombre']} ✅")
        return redirect(url_for("llamadas.historial", cliente_id=cliente_id))

        # Si es GET, simplemente mostramos el formulario
    return render_template("nueva_llamada.html", cliente=cliente)


