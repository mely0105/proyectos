# FriendlyEats - FastAPI 
Este proyecto es una aplicación web local para gestionar y consultar restaurantes. Está desarrollada con **FastAPI**, **Jinja2**, **JavaScript** y utiliza **Firestore** (a través de su emulador local) como base de datos.

******************************************************

# Requisitos necesarios:

- **Python 3.10** o superior.
- **Node.js** y **NPM** (para el emulador de Firebase).
- **Firebase CLI** (`npm install -g firebase-tools`).

******************************************************

# Configuración del Entorno Local

# 1. Clonar el repositorio e instalar dependencias
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Linux/macOS:
source .venv/bin/activate
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt