from flask import Flask, render_template, session, redirect, url_for
from app.routes import dashboard
from app.routes.auth import auth
from flask import session, redirect, url_for, render_template
from app.routes.clientes import clientes_bp 
from app.routes.dashboard import dashboard




def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    # registrar rutas (blueprints)
    app.register_blueprint(auth)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(dashboard)

    @app.route("/")
    def inicio():
        if "usuario" not in session:
            return redirect(url_for("auth.login"))

        return redirect(url_for("dashboard.home"))

    return app