from app import create_app

# Creamos la instancia de la aplicación llamando a la "fábrica" de aplicaciones
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    