# 📞 CRM Contact Center - Gestión Integral de Clientes

Este es un sistema de **CRM (Customer Relationship Management)** diseñado específicamente para las necesidades de un **Contact Center**. Permite la gestión profesional de prospectos, control de acceso por roles y búsqueda ágil de clientes.

Este proyecto forma parte de mi portafolio como estudiante de **Ingeniería de Software y Datos**, demostrando habilidades en desarrollo backend, seguridad y diseño de interfaces corporativas.

---

## 🚀 Funcionalidades Principales

- **Autenticación Segura:** Sistema de Login y Registro con encriptación de contraseñas mediante `werkzeug.security`.
- **Gestión de Roles:** Diferenciación entre perfiles de **Administrador** (control total) y **Agente** (operación diaria).
- **Módulo de Clientes (CRUD):** Registro, visualización y eliminación de clientes de forma dinámica.
- **Buscador Dual Inteligente:** Localización inmediata de clientes por nombre o por número de teléfono/celular (vital para la agilidad en llamadas).
- **Diseño Profesional:** Interfaz limpia y responsiva construida con **Bootstrap 5** y **FontAwesome**, optimizada para la productividad del agente.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.x con el framework **Flask**.
- **Base de Datos:** SQLite3 (Estructura relacional optimizada).
- **Frontend:** HTML5, CSS3 (Custom Corporate Style), Jinja2 y Bootstrap 5.
- **Seguridad:** Encriptación PBKDF2 para el manejo de credenciales.
- **Control de Versiones:** Git y GitHub.

---

## 📂 Estructura del Proyecto

El proyecto sigue el **Patrón de Fábrica** y está organizado mediante **Blueprints** para facilitar su escalabilidad:

```text
crm_contact_center/
├── app/
│   ├── models/          # Lógica de base de datos (SQL)
│   ├── routes/          # Controladores y lógica de rutas
│   ├── static/          # Archivos CSS y recursos visuales
│   └── templates/       # Vistas HTML (Jinja2)
├── database/            # Archivo de base de datos y scripts de inicialización
├── run.py               # Punto de entrada de la aplicación
└── .gitignore           # Configuración de archivos excluidos del repositorio
