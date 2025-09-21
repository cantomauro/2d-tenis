# utilidades para rutas a assets/ (cargar imágenes/fuentes con rutas relativas seguras).

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(os.path.dirname(BASE_DIR), "assets")

def asset(*parts):  # asset("players", "idle_se.png")
    return os.path.join(ASSETS, *parts)
