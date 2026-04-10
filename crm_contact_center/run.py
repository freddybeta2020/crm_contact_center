from app import create_app
from flask import session, redirect, url_for, render_template


# 1. Creamos la instancia de la aplicación llamando a la "fábrica" de aplicaciones
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    
    @app.route("/")
    def inicio():
       # Si no hay un correo guardado en la  (sesión),va al login
     if "usuario" not in session:
        return redirect(url_for("auth.login"))
     # Si ya está logueado, lo mandamos al index
     return render_template("index.html")
    