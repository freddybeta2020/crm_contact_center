from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# Importamos todas las funciones necesarias del modelo
from app.models.cliente import (
    crear_cliente,
    obtener_clientes,
    eliminar_cliente,
    buscar_clientes,
    obtener_cliente_por_id,
    actualizar_cliente
)

# Definimos el blueprint (asegúrate que este nombre coincida con el registro en __init__.py)
clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route("/clientes")
def lista_clientes():
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    termino = request.args.get('q', '')

    if termino:
        datos = buscar_clientes(termino)
    else:
        datos = obtener_clientes()

    return render_template("clientes.html", clientes=datos, busqueda=termino)


@clientes_bp.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
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
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "admin":
        flash("Acceso denegado: No tienes permiso para eliminar registros 🚫")
        return redirect(url_for("clientes.lista_clientes"))

    eliminar_cliente(id)
    flash(f"Cliente con ID {id} eliminado correctamente ✅")
    return redirect(url_for("clientes.lista_clientes"))


@clientes_bp.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    # 1. Buscamos el cliente para llenar el formulario de edición
    cliente = obtener_cliente_por_id(id)

    if request.method == "POST":
        # 2. Recibimos los cambios del formulario
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        email = request.form["email"]

        # 3. Guardamos los cambios en la DB
        actualizar_cliente(id, nombre, telefono, email)

        flash(f"Información de {nombre} actualizada con éxito ✨")
        return redirect(url_for("clientes.lista_clientes"))

    # Mostramos el formulario pasando el objeto 'cliente'
    return render_template("editar_cliente.html", cliente=cliente)
