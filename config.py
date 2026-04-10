import os

# En desarrollo usa la clave por defecto; en producción define la variable de entorno SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY", "clave_super_secreta_123")