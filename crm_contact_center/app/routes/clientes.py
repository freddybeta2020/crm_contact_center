from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# IMPORTANTE: Importamos 'buscar_clientes' que es la que sabe filtrar
from app.models.cliente import crear_cliente, obtener_clientes, eliminar_cliente, buscar_clientes

# Definimos el blueprint
clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route("/clientes")
def lista_clientes():
    """
    Ruta única para mostrar la lista. 
    Maneja tanto la vista normal como la búsqueda filtrada.
    """
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    # 1. Capturamos lo que el usuario escribió en el buscador (si existe)
    termino = request.args.get('q', '')

    # 2. Lógica de decisión:
    if termino:
        # Si hay algo escrito, usamos la función de BUSCAR
        datos = buscar_clientes(termino)
    else:
        # Si está vacío, traemos TODO
        datos = obtener_clientes()

    return render_template("clientes.html", clientes=datos, busqueda=termino)


@clientes_bp.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    """Ruta para crear un cliente nuevo."""
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        email = request.form["email"]

        crear_cliente(nombre, telefono, email)
        flash(f"Cliente {nombre} registrado con éxito ✅")
        return redirect(url_for("clientes.lista_clientes"))

    return render_template("nuevo_cliente.html")


@clientes_bp.route("/clientes/eliminar/<int:id>")
def eliminar(id):
    """Ruta segura para borrar un cliente."""
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    # Seguridad de rol
    if session.get("rol") != "admin":
        flash("Acceso denegado: No tienes permiso para eliminar registros 🚫")
        return redirect(url_for("clientes.lista_clientes"))

    eliminar_cliente(id)
    flash(f"Cliente con ID {id} eliminado correctamente ✅")
    return redirect(url_for("clientes.lista_clientes"))