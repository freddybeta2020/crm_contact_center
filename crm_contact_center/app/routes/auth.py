from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.user import buscar_usuario
from app.models.user import crear_usuario
from flask import flash

# Creamos un Blueprint para las rutas de autenticación
auth = Blueprint('auth', __name__)
@auth.route("/login", methods=["GET", "POST"])
def login():
    print("ENTRÓ A LOGIN")

# Si el método es POST, significa que el usuario envió el formulario de login
    if request.method == "POST":
        print("ES POST 🔥")

        email = request.form["email"]
        password = request.form["password"]

        print("EMAIL:", email)
        print("PASSWORD:", password)

        user = buscar_usuario(email, password)
        print("RESULTADO BD:", user)
# Si el usuario existe y la contraseña es correcta, lo logueamos        
        user = buscar_usuario(email, password)
        
        if user:
            session["usuario"] = user["email"]  # Guardar el ID del usuario en la sesión
            session["rol"] = user["rol"]  # Guardar el rol del usuario en la sesión
            
            if user["rol"] == "admin":
                return redirect(url_for("dashboard.home"))
            else:
                return redirect(url_for("dashboard.home"))
        else:
            return("Credenciales incorrectas ❌")

    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
# Ruta para registrar un nuevo usuario
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        crear_usuario(email, password)
        
        
        flash("Usuario creado correctamente ✅")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

# Ruta para cerrar sesión

@auth.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("auth.login"))  