# mapea teclado a vector de movimiento en mundo (normaliza y usa dt).

import pygame

from core.physics.vector import normalize


def read_player_inputs(keys, mapping):
    dx = (1 if keys[mapping["right"]] else 0) - (1 if keys[mapping["left"]] else 0)
    dy = (1 if keys[mapping["down"]] else 0) - (1 if keys[mapping["up"]] else 0)
    if dx == 0 and dy == 0:
        return 0.0, 0.0
    return normalize(dx, dy)
