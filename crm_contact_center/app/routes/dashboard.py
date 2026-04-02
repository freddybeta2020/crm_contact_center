from flask import Blueprint, render_template, session, redirect, url_for
from app.models.cliente import contar_clientes

# Cambiamos el nombre a dashboard_bp para ser consistentes con clientes_bp
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/dashboard")
def home():
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    # Obtenemos el dato real de la base de datos
    total = contar_clientes()

    # Pasamos también el rol por si quieres mostrar botones especiales solo al admin
    rol_usuario = session.get("rol")

    return render_template("index.html", total_clientes=total, rol=rol_usuario)