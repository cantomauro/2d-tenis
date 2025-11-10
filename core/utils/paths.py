# utilidades para rutas a assets/ (cargar imágenes/fuentes con rutas relativas seguras).

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
ASSETS = os.path.join(PROJECT_ROOT, "assets")


def asset(*parts):  # asset("players", "idle_se.png")
    return os.path.join(ASSETS, *parts)


def project_path(*parts):
    """Ruta absoluta relativa a la raíz del proyecto."""
    return os.path.join(PROJECT_ROOT, *parts)
