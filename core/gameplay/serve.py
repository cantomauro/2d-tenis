"""Lógica de saque y puntaje."""

import random

from core.config import (
    COURT_X,
    COURT_Y,
    COURT_W,
    COURT_H,
    SERVE_DELAY,
    TARGET_SCORE,
)
from core.app.shared import COURT_BOUNDS


def prepare_serve(ball, towards_p2: bool, delay: float = SERVE_DELAY):
    """reposiciona la pelota y arranca el temporizador de saque."""
    ball.x = COURT_X + COURT_W / 2
    ball.y = COURT_Y + COURT_H / 2
    ball.vx = 0.0
    ball.vy = 0.0
    return delay, towards_p2


def apply_serve_velocity(ball, towards_p2: bool):
    """asigna una velocidad inicial pseudoaleatoria a la pelota."""
    speed = 260
    ball.vx = random.choice([-1, 1]) * random.uniform(0.4 * speed, 0.8 * speed)
    vy_mag = random.uniform(0.6 * speed, 1.0 * speed)
    ball.vy = -vy_mag if towards_p2 else +vy_mag


def check_point(ball, p1_score: int, p2_score: int):
    """evalúa si hay punto y devuelve el nuevo estado."""
    top_goal = ball.y - ball.radius <= COURT_BOUNDS.top
    bot_goal = ball.y + ball.radius >= COURT_BOUNDS.bottom

    if top_goal:
        p1_score += 1
        return p1_score, p2_score, True, True, "P1"
    if bot_goal:
        p2_score += 1
        return p1_score, p2_score, True, False, "P2"
    return p1_score, p2_score, False, None, None


def reached_target(p1_score, p2_score):
    """Indica si algún jugador alcanzó el puntaje objetivo."""
    return p1_score >= TARGET_SCORE or p2_score >= TARGET_SCORE

