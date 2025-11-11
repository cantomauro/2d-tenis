"""Helpers relacionados a la gestión de jugadores dentro del partido."""

from core.config import COURT_X, COURT_Y, COURT_W, COURT_H
from core.app.shared import COURT_BOUNDS


def clamp_player_to_half(player, top_half: bool):
    """restringe al jugador a su mitad de la cancha."""
    r = player.hit_rect
    min_x = COURT_BOUNDS.left + r.width / 2
    max_x = COURT_BOUNDS.right - r.width / 2
    mid = COURT_BOUNDS.top + COURT_BOUNDS.height / 2

    if top_half:
        min_y = COURT_BOUNDS.top + r.height / 2
        max_y = mid - r.height / 2
    else:
        min_y = mid + r.height / 2
        max_y = COURT_BOUNDS.bottom - r.height / 2

    player.x = max(min_x, min(max_x, player.x))
    player.y = max(min_y, min(max_y, player.y))


def reset_players_to_spawn(p1, p2):
    """ubica a cada jugador en su posición inicial."""
    mid_x = COURT_X + COURT_W / 2
    p1.x, p1.y = mid_x, COURT_Y + COURT_H * 0.85
    p2.x, p2.y = mid_x, COURT_Y + COURT_H * 0.15
    p1.vx = p1.vy = 0.0
    p2.vx = p2.vy = 0.0
    p1.home_x, p1.home_y = p1.x, p1.y
    p2.home_x, p2.home_y = p2.x, p2.y
    clamp_player_to_half(p1, top_half=False)
    clamp_player_to_half(p2, top_half=True)

