# colisión círculo-rect para pelota–jugador, rebotes con bordes, cálculo de normal y reflexión.

from core.utils.math2d import reflect

def circle_rect_collision(cx, cy, r, rect):
    # punto más cercano del rect al centro
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top,  min(cy, rect.bottom))
    dx, dy = cx - closest_x, cy - closest_y
    return (dx*dx + dy*dy) <= (r*r), dx, dy

def ball_vs_bounds(ball, bounds_rect):
    # Rebote contra límites del mundo (cancha)
    bounced = False
    if ball.x - ball.radius < bounds_rect.left:
        ball.x = bounds_rect.left + ball.radius; ball.vx *= -1; bounced = True
    if ball.x + ball.radius > bounds_rect.right:
        ball.x = bounds_rect.right - ball.radius; ball.vx *= -1; bounced = True
    if ball.y - ball.radius < bounds_rect.top:
        ball.y = bounds_rect.top + ball.radius; ball.vy *= -1; bounced = True
    if ball.y + ball.radius > bounds_rect.bottom:
        ball.y = bounds_rect.bottom - ball.radius; ball.vy *= -1; bounced = True
    return bounced

def ball_vs_player(ball, player):
    hit, dx, dy = circle_rect_collision(ball.x, ball.y, ball.radius, player.hit_rect)
    if not hit:
        return False
    # normal desde punto de contacto hacia centro de la pelota
    # decidir eje de mayor penetración: simple usando |dx| vs |dy|
    if abs(dx) > abs(dy):
        nx, ny = (1, 0) if dx > 0 else (-1, 0)
    else:
        nx, ny = (0, 1) if dy > 0 else (0, -1)
    ball.vx, ball.vy = reflect(ball.vx, ball.vy, nx, ny)
    return True
