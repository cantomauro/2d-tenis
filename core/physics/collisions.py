# core/physics/collisions.py
from math import copysign
from core.config import BALL_HIT_COOLDOWN, MAX_HIT_ANGLE_X, BALL_HIT_SPEED

def ball_vs_player(ball, player, court_rect):
    """
    - player.hit_rect está en plano 2D
    - court_rect es el rect de la cancha. solo para saber mitad top/ bottom
    """
    r = player.hit_rect

    # punto más cercano del rectángulo al centro de la bola
    closest_x = max(r.left, min(ball.x, r.right))
    closest_y = max(r.top,  min(ball.y, r.bottom))
    dx = ball.x - closest_x
    dy = ball.y - closest_y
    if (dx*dx + dy*dy) > (ball.radius * ball.radius):
        return  # no hay colisión

    # evita colisiones múltiples seguidas
    if ball.hit_cooldown > 0:
        separate_ball_from_player(ball, player)
        return

    # p2 arriba y p1 abajo de la cancha
    court_mid_y = court_rect.top + court_rect.height * 0.5
    is_p2 = (r.centery < court_mid_y)

    # P2 pega hacia abajo (+y) y P1 hacia arriba (-y)
    dir_y = 1.0 if is_p2 else -1.0

    # dirección x según dónde impacta en el ancho del jugador
    rel = (ball.x - r.centerx) / (r.width * 0.5)
    rel = max(-1.0, min(1.0, rel))  # clamp
    dir_x = rel * MAX_HIT_ANGLE_X

    # evita trayectorias verticales
    if abs(dir_x) < 0.05:
        dir_x = copysign(0.05, dir_x if dir_x != 0 else 1)

    #  velocidad fija
    ball.set_velocity_dir(BALL_HIT_SPEED, dir_x, dir_y)

    #  hitter + cooldown
    ball.last_hitter = "P2" if is_p2 else "P1"
    ball.hit_cooldown = BALL_HIT_COOLDOWN

    # separa la bola del jugador
    separate_ball_from_player(ball, player)


def separate_ball_from_player(ball, player):
    """ saca la bola fuera del rect del jugador empujándola en su dirección actual."""
    push = max(1.0, ball.radius)
    norm = (ball.vx**2 + ball.vy**2) ** 0.5
    if norm < 1e-6:
        dx, dy = 0.0, -1.0
    else:
        dx, dy = (ball.vx / norm), (ball.vy / norm)

    r = player.hit_rect
    for _ in range(6):
        if r.collidepoint(ball.x, ball.y):
            ball.x += dx * push
            ball.y += dy * push
        else:
            break
