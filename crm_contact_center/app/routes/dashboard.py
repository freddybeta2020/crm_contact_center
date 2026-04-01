from flask import Blueprint, render_template, session, redirect, url_for
from app.models.cliente import contar_clientes

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/dashboard")
def home():
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    total_clientes = contar_clientes()

    return render_template("index.html", total_clientes=total_clientes)