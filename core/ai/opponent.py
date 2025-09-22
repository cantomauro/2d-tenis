# core/ai/opponent.py
from core.utils.math2d import normalize

def ai_drive(player_ai, ball, dt):
    """
    IA simple: intenta alinear x e y con la pelota y aplica movimiento.
    El clamp a la mitad de cancha lo hace main.py (desacoplado).
    """
    dx = ball.x - player_ai.x
    dy = ball.y - player_ai.y

    # zona muerta
    dead = 6.0
    if abs(dx) < dead: dx = 0.0
    if abs(dy) < dead: dy = 0.0

    if dx == 0.0 and dy == 0.0:
        ndx, ndy = 0.0, 0.0
    else:
        ndx, ndy = normalize(dx, dy)

    # pequeño boost si la pelota va "hacia abajo"
    boost = 1.15 if ball.vy > 0 else 1.0

    player_ai.apply_input(ndx * boost, ndy * boost, dt)
