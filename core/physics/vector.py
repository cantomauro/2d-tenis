"""Operaciones vectoriales básicas para lógica de movimiento."""

from math import hypot


def normalize(dx: float, dy: float, eps: float = 1e-6):
    """Normaliza un vector 2D, con protección a magnitudes pequeñas."""
    length = max(eps, hypot(dx, dy))
    return dx / length, dy / length

