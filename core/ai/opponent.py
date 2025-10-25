# core/ai/opponent.py
from core.utils.math2d import normalize


def ai_drive(player_ai, ball, dt):
    """
    IA simple: sigue la pelota cuando está en su campo y se repliega a su base cuando la bola está en campo rival.
    """
    target_x = ball.x
    target_y = ball.y

    # Si la pelota está en la mitad rival, replegarse hacia su zona de espera
    if ball.y > player_ai.y + 36:
        home_y = getattr(player_ai, "home_y", player_ai.y)
        home_x = getattr(player_ai, "home_x", player_ai.x)
        target_y = home_y
        target_x = home_x + (ball.x - home_x) * 0.35

    dx = target_x - player_ai.x
    dy = target_y - player_ai.y

    dead = 6.0
    if abs(dx) < dead:
        dx = 0.0
    if abs(dy) < dead:
        dy = 0.0

    if dx == 0.0 and dy == 0.0:
        ndx, ndy = 0.0, 0.0
    else:
        ndx, ndy = normalize(dx, dy)

    boost = 1.15 if ball.vy > 0 else 1.0
    player_ai.apply_input(ndx * boost, ndy * boost, dt)
