# ----------------------------------------------
# Juego de tenis 2D con render isométrico
# - 1 jugador vs IA o 2 jugadores en el mismo teclado
# - Colisiones y rebotes básicos
# - Dibujo isométrico y orden por profundidad
# - Marcador simple con pygame.font
# ----------------------------------------------

# IMPORTS
import sys
import random
import pygame

from core.ai.opponent import ai_drive
from core.iso.projection import world_to_iso
from core.entities.player import Player
from core.entities.ball import Ball
from core.render.court import Court
from core.render.hud import Hud
from core.systems.input_controller import read_player_inputs
from core.physics.collisions import ball_vs_player
from core.utils.math2d import clamp
# FIN IMPORTS

# PARAMETROS BASICOS DEL JUEGO (PANTALLA Y FPS)
SCREEN_W, SCREEN_H = 1024, 768
FPS = 60

# COLORES Y CONSTANTE DEL DELAY DEL SAQUE (en segundos)
SERVE_DELAY = 1.0
P1_MSG_COLOR = (64, 160, 255)   # azul para P1
P2_MSG_COLOR = (220, 70, 70)    # rojo para P2 (IA)

# MUNDO / CANCHA
COURT_X, COURT_Y = 0, 0
COURT_W, COURT_H = 380, 600  # ANCHO y ALTO de la cancha en "mundo"
COURT_BOUNDS = pygame.Rect(COURT_X, COURT_Y, COURT_W, COURT_H)

def auto_iso_offset(world_rect, screen_w, screen_h, backshift=0):
#ajusta el offset (ox, oy) de la proyección isométrica para centrar/posicionar la cancha.
# backshift < 0 => empuja hacia el "fondo" (arriba en pantalla)
    cx = world_rect.left + world_rect.width / 1.65
    cy = world_rect.top  + world_rect.height / 1.75
    ox = (screen_w // 2) - (cx - cy)
    oy = (screen_h // 1.75) - ((cx + cy) / 2) + backshift
    return int(ox), int(oy)

# DIBUJA LA PROYECCION ISOMETRICA CENTRADA EN LA PANTALLA
ISO_OFFSET_X, ISO_OFFSET_Y = auto_iso_offset(COURT_BOUNDS, SCREEN_W, SCREEN_H, backshift=-40)

# controles: J1 (WASD) y J2 (FLECHAS)
P1_KEYS = {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s}
P2_KEYS = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN}

# modo de juego (True = IA controla al jugador 2; False = humano)
P2_IS_AI = True

# PUNTAJE PARA TERMINAR EL JUEGO
TARGET_SCORE = 7

def clamp_player_to_half(player: Player, top_half: bool):
    """Mantiene al jugador en SU mitad de la cancha (evita cruzar la red)."""
    r = player.hit_rect
    # límites X para que no se salga por los laterales (considerando el tamaño del hitbox)
    min_x = COURT_BOUNDS.left + r.width / 2
    max_x = COURT_BOUNDS.right - r.width / 2

    # línea media
    mid = COURT_BOUNDS.top + COURT_BOUNDS.height / 2

    if top_half:
        # P2 (mitad superior)
        min_y = COURT_BOUNDS.top + r.height / 2
        max_y = mid - r.height / 2
    else:
        # P1 (mitad inferior)
        min_y = mid + r.height / 2
        max_y = COURT_BOUNDS.bottom - r.height / 2

    player.x = clamp(player.x, min_x, max_x)
    player.y = clamp(player.y, min_y, max_y)

def reset_players_to_spawn(p1: Player, p2: Player):
    """Reubica jugadores a posiciones iniciales y los clampa a su mitad."""
    mid_x = COURT_X + COURT_W / 2
    p1.x, p1.y = mid_x, COURT_Y + COURT_H * 0.85
    p2.x, p2.y = mid_x, COURT_Y + COURT_H * 0.15
    p1.vx = p1.vy = 0.0
    p2.vx = p2.vy = 0.0
    clamp_player_to_half(p1, top_half=False)
    clamp_player_to_half(p2, top_half=True)

def prepare_serve(ball: Ball, towards_p2: bool, delay: float = SERVE_DELAY):
    """Deja la pelota QUIETA en el centro y programa el saque tras 'delay'."""
    ball.x = COURT_X + COURT_W / 2
    ball.y = COURT_Y + COURT_H / 2
    ball.vx = 0.0
    ball.vy = 0.0
    return delay, towards_p2  # (serve_timer, serve_dir_p2)

def apply_serve_velocity(ball: Ball, towards_p2: bool):
    """
    Asigna velocidad de saque:
    - towards_p2=True  -> hacia ARRIBA (P2) => vy NEGATIVO
    - towards_p2=False -> hacia ABAJO (P1)  => vy POSITIVO
    """
    speed = 260
    ball.vx = random.choice([-1, 1]) * random.uniform(0.4 * speed, 0.8 * speed)
    vy_mag = random.uniform(0.6 * speed, 1.0 * speed)
    ball.vy = -vy_mag if towards_p2 else +vy_mag

def check_point(ball: Ball, p1_score: int, p2_score: int):
    """
    Retorna: (p1_score, p2_score, scored: bool, next_towards_p2: bool|None, scorer: str|None)
    - top_goal  (sale por arriba)  => punto P1
    - bottom    (sale por abajo)   => punto P2
    """
    top_goal = ball.y - ball.radius <= COURT_BOUNDS.top
    bot_goal = ball.y + ball.radius >= COURT_BOUNDS.bottom

    if top_goal:
        p1_score += 1
        return p1_score, p2_score, True, True, "P1"   # próximo saque orientado hacia P2 (arriba)
    if bot_goal:
        p2_score += 1
        return p1_score, p2_score, True, False, "P2"  # próximo saque orientado hacia P1 (abajo)
    return p1_score, p2_score, False, None, None

# loop
def main():
    pygame.init()
    pygame.display.set_caption("Tenis 2D")
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()

    # FUENTE para HUD
    font = pygame.font.Font(None, 32)
    hud = Hud(font)

    # CANCHA (mundo) y su renderer
    court = Court(COURT_BOUNDS, screen_offset=(ISO_OFFSET_X, ISO_OFFSET_Y))

    # ENTIDADES: jugadores y pelota
    p1 = Player(COURT_X + COURT_W / 2, COURT_Y + COURT_H * 0.85, speed=190, is_ai=False, name="P1")
    p2 = Player(COURT_X + COURT_W / 2, COURT_Y + COURT_H * 0.15, speed=175, is_ai=P2_IS_AI, name="P2")
    ball = Ball(COURT_X + COURT_W / 2, COURT_Y + COURT_H / 2, vx=0, vy=0, radius=30, visual_radius=12)

    # Quién saca y primer saque programado
    server = "P1"  # arranca sacando P1
    serve_timer, serve_dir_p2 = prepare_serve(ball, towards_p2=(server == "P1"))
    last_point_scorer = None  # no mostrar cartel al inicio

    # PUNTAJE
    p1_score = 0
    p2_score = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # segundos por frame

        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # DELAY LUEGO DEL TANTO: pelota quieta hasta vencer el timer
        if serve_timer > 0:
            serve_timer -= dt
            if serve_timer <= 0:
                apply_serve_velocity(ball, towards_p2=serve_dir_p2)

        # Durante el delay bloqueamos movimiento
        serve_locked = (serve_timer > 0)

        # INPUT / IA
        if not serve_locked:
            # P1 humano
            dx1, dy1 = read_player_inputs(keys, P1_KEYS)
            p1.apply_input(dx1, dy1, dt)
            clamp_player_to_half(p1, top_half=False)

            # P2 humano o IA
            if not p2.is_ai:
                dx2, dy2 = read_player_inputs(keys, P2_KEYS)
                p2.apply_input(dx2, dy2, dt)
                clamp_player_to_half(p2, top_half=True)
            else:
                ai_drive(p2, ball, dt)
                clamp_player_to_half(p2, top_half=True)
        else:
            # Aun bloqueados, forcemos a quedar dentro de cada mitad
            clamp_player_to_half(p1, top_half=False)
            clamp_player_to_half(p2, top_half=True)

        # UPDATE lógicos
        ball.update(dt)

        # Rebotes LATERALES (izquierda/derecha) — top/bottom cuentan punto
        if ball.x - ball.radius <= COURT_BOUNDS.left:
            ball.x = COURT_BOUNDS.left + ball.radius
            ball.vx *= -1
        elif ball.x + ball.radius >= COURT_BOUNDS.right:
            ball.x = COURT_BOUNDS.right - ball.radius
            ball.vx *= -1

        # Colisiones pelota–jugadores
        ball_vs_player(ball, p1)
        ball_vs_player(ball, p2)

        # PUNTOS y SAQUE PROGRAMADO
        p1_score, p2_score, scored, _next_towards_p2, scorer = check_point(ball, p1_score, p2_score)
        if scored:
            # El que anota, SACA
            server = scorer  # "P1" o "P2"

            # Programar el saque según QUIÉN saca (dirección hacia el rival)
            serve_timer, serve_dir_p2 = prepare_serve(ball, towards_p2=(server == "P1"))

            # Cartel "PUNTO PARA ..."
            last_point_scorer = scorer

            # ¿Victoria de la partida?
            if p1_score >= TARGET_SCORE or p2_score >= TARGET_SCORE:
                # Reset de partida
                p1_score = 0
                p2_score = 0
                reset_players_to_spawn(p1, p2)

                # Reinicia el servidor (por ahora P1)
                server = "P1"
                serve_timer, serve_dir_p2 = prepare_serve(ball, towards_p2=(server == "P1"))
                last_point_scorer = None  # no mostrar cartel en el nuevo inicio

        # RENDER (un único bloque)
        screen.fill((18, 18, 22))
        court.draw(screen, world_to_iso)

        entities = [p1, p2, ball]
        entities.sort(key=lambda e: e.depth_key())
        for e in entities:
            e.draw(screen, ISO_OFFSET_X, ISO_OFFSET_Y)

        hud.draw_score(screen, p1_score, p2_score, SCREEN_W)

        # Cartel "PUNTO PARA ..." durante el delay de saque
        if serve_timer > 0 and last_point_scorer:
            msg = f"PUNTO PARA {last_point_scorer}"
            color = P1_MSG_COLOR if last_point_scorer == "P1" else P2_MSG_COLOR
            hud.draw_center_message(screen, msg, color, SCREEN_W, SCREEN_H)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
