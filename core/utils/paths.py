# utilidades para rutas a assets/ (cargar imágenes/fuentes con rutas relativas seguras).

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if hasattr(sys, "_MEIPASS"):
    PROJECT_ROOT = sys._MEIPASS  # estamos dentro del ejecutable
else:
    PROJECT_ROOT = os.path.dirname(BASE_DIR)  # ejecución normal desde el repo

ASSETS = os.path.join(PROJECT_ROOT, "assets")


def asset(*parts):
    return os.path.join(ASSETS, *parts)


def project_path(*parts):
    """Ruta absoluta relativa a la raíz del proyecto."""
    return os.path.join(PROJECT_ROOT, *parts)