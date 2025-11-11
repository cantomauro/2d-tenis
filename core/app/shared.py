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

PLAYER_SPRITE_SIZE = (64, 64)
BALL_VISUAL_RADIUS = 12
TRIBUNE_IMAGE_PATH = asset("crowd", "crowd-happy.png")

PLAYER_FRAME_PATHS = {
    "blue": [
        asset("players", "blue", "blue-0.png"),
        asset("players", "blue", "blue-1.png"),
        asset("players", "blue", "blue-2.png"),
    ],
    "red": [
        asset("players", "red", "red-0.png"),
        asset("players", "red", "red-1.png"),
        asset("players", "red", "red-2.png"),
    ],
}

_PLAYER_FRAME_CACHE: dict[str, list[pygame.Surface]] = {}


def load_player_frames(color: str) -> list[pygame.Surface]:
    """
    Devuelve (y cachea) la secuencia de frames para el color indicado.
    Se asume que pygame ya inicializó display antes de llamar a esta función.
    """
    key = color.lower()
    if key not in PLAYER_FRAME_PATHS:
        raise ValueError(f"Color de jugador desconocido: '{color}'")
    if key in _PLAYER_FRAME_CACHE:
        return _PLAYER_FRAME_CACHE[key]

    frames: list[pygame.Surface] = []
    for path in PLAYER_FRAME_PATHS[key]:
        try:
            frames.append(pygame.image.load(path).convert_alpha())
        except Exception as exc:
            print(f"[shared.load_player_frames] No pude cargar '{path}': {exc}")
            placeholder = pygame.Surface(PLAYER_SPRITE_SIZE, pygame.SRCALPHA)
            placeholder.fill((255, 0, 255, 160))
            frames.append(placeholder)
    _PLAYER_FRAME_CACHE[key] = frames
    return frames


FONT_PATH = asset("fonts", "PressStart2P-Regular.ttf")


def auto_iso_offset(world_rect, screen_w, screen_h, backshift=0):
    cx = world_rect.left + world_rect.width / 1.65
    cy = world_rect.top + world_rect.height / 1.75
    ox = (screen_w // 2) - (cx - cy)
    oy = (screen_h // 1.75) - ((cx + cy) / 2) + backshift
    return int(ox), int(oy)


ISO_OFFSET_X, ISO_OFFSET_Y = auto_iso_offset(COURT_BOUNDS, SCREEN_W, SCREEN_H, backshift=-40)
