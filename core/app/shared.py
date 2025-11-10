# Helpers y constantes compartidas entre escenas.
import pygame

from core.config import (
    SCREEN_W,
    SCREEN_H,
    COURT_X,
    COURT_Y,
    COURT_W,
    COURT_H,
)
from core.utils.paths import asset

COURT_BOUNDS = pygame.Rect(COURT_X, COURT_Y, COURT_W, COURT_H)

P1_KEYS = {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s}
P2_KEYS = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
}

PLAYER_SPRITE_SIZE = (40, 40)
BALL_VISUAL_RADIUS = 12
BALL_ANIM_FRAMES = [
    asset("equipment", "ball_tennis1.png"),
    asset("equipment", "ball_tennis2.png"),
]
BALL_FRAME_DURATION = 0.16

PLAYER_OVERLAY_CONFIG = {
    "blue": {
        "body": asset("players", "blue", "jugador1.png"),
        "leg": asset("players", "blue", "pie.png"),
        "hand": asset("players", "blue", "mano.png"),
        "leg_offset": (0, 8),
        "hand_offset": (4, -6),
        "leg_stride": 3.5,
        "leg_rotation_range": (-12.0, 12.0),
        "leg_scale": 0.7,
        "hand_scale": 0.45,
    },
    "red": {
        "body": asset("players", "red", "jugador2.png"),
        "leg": asset("players", "red", "pie.png"),
        "hand": asset("players", "red", "mano.png"),
        "leg_offset": (0, 8),
        "hand_offset": (-3, -6),
        "leg_stride": 3.5,
        "leg_rotation_range": (-12.0, 12.0),
        "leg_scale": 0.7,
        "hand_scale": 0.45,
    },
}
FONT_PATH = asset("fonts", "PressStart2P-Regular.ttf")


def auto_iso_offset(world_rect, screen_w, screen_h, backshift=0):
    cx = world_rect.left + world_rect.width / 1.65
    cy = world_rect.top + world_rect.height / 1.75
    ox = (screen_w // 2) - (cx - cy)
    oy = (screen_h // 1.75) - ((cx + cy) / 2) + backshift
    return int(ox), int(oy)


ISO_OFFSET_X, ISO_OFFSET_Y = auto_iso_offset(COURT_BOUNDS, SCREEN_W, SCREEN_H, backshift=-40)
