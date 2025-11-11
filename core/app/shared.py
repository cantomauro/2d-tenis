# Helpers y constantes compartidas entre escenas.
import pygame

from core.config import (
    SCREEN_W,
    SCREEN_H,
    COURT_X,
    COURT_Y,
    COURT_W,
    COURT_H,
    CROWD_BG_SCALE,
    CROWD_BG_OFFSET,
    CROWD_SIDE_SCALE,
    CROWD_SIDE_OFFSET,
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
BALL_VISUAL_RADIUS = 10

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

CROWD_LAYER_DEFS = [
    {
        "path": asset("crowd", "crowd.png"),
        "scale": CROWD_BG_SCALE,
        "offset": CROWD_BG_OFFSET,
        "anchor": "center",
        "scale_mode": "screen",
    },
    {
        "path": asset("crowd", "crowd2.png"),
        "scale": CROWD_SIDE_SCALE,
        "offset": CROWD_SIDE_OFFSET,
        "anchor": "topright",
        "scale_mode": "image",
    },
]

_CROWD_LAYER_CACHE: list[tuple[pygame.Surface, tuple[int, int]]] | None = None


def load_crowd_layers() -> list[tuple[pygame.Surface, tuple[int, int]]]:
    """Carga y cachea todas las capas de público definidas en CROWD_LAYER_DEFS."""
    global _CROWD_LAYER_CACHE
    if _CROWD_LAYER_CACHE is not None:
        return _CROWD_LAYER_CACHE

    layers: list[tuple[pygame.Surface, tuple[int, int]]] = []
    for conf in CROWD_LAYER_DEFS:
        surface = _load_crowd_surface(conf["path"], conf["scale"], conf["scale_mode"])
        if surface is None:
            continue
        anchor_pos = _compute_anchor(surface.get_width(), surface.get_height(), conf["anchor"])
        offset = (
            anchor_pos[0] + conf["offset"][0],
            anchor_pos[1] + conf["offset"][1],
        )
        layers.append((surface, offset))

    _CROWD_LAYER_CACHE = layers
    return _CROWD_LAYER_CACHE


def _load_crowd_surface(path: str, scale: float, scale_mode: str) -> pygame.Surface | None:
    try:
        image = pygame.image.load(path).convert_alpha()
    except Exception as exc:
        print(f"[shared.load_crowd_layers] No pude cargar '{path}': {exc}")
        return None

    scale = max(0.1, scale)
    if scale_mode == "screen":
        target_w = max(1, int(SCREEN_W * scale))
        target_h = max(1, int(SCREEN_H * scale))
    else:
        width, height = image.get_size()
        target_w = max(1, int(width * scale))
        target_h = max(1, int(height * scale))

    if image.get_size() != (target_w, target_h):
        image = pygame.transform.smoothscale(image, (target_w, target_h))
    return image


def _compute_anchor(width: int, height: int, anchor: str) -> tuple[int, int]:
    if anchor == "center":
        return (SCREEN_W - width) // 2, (SCREEN_H - height) // 2
    if anchor == "topright":
        return SCREEN_W - width, 0
    return 0, 0


def auto_iso_offset(world_rect, screen_w, screen_h, backshift=0):
    cx = world_rect.left + world_rect.width / 1.65
    cy = world_rect.top + world_rect.height / 1.75
    ox = (screen_w // 2) - (cx - cy)
    oy = (screen_h // 1.75) - ((cx + cy) / 2) + backshift
    return int(ox), int(oy)


ISO_OFFSET_X, ISO_OFFSET_Y = auto_iso_offset(COURT_BOUNDS, SCREEN_W, SCREEN_H, backshift=-40)
