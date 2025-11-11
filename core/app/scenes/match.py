"""Escena principal del partido."""

import pygame

from core.config import (
    FPS,
    SCREEN_W,
    SCREEN_H,
    P1_MSG_COLOR,
    P2_MSG_COLOR,
    TARGET_SCORE,
)
from core.app.shared import (
    COURT_BOUNDS,
    ISO_OFFSET_X,
    ISO_OFFSET_Y,
    PLAYER_SPRITE_SIZE,
    BALL_VISUAL_RADIUS,
    P1_KEYS,
    P2_KEYS,
    FONT_PATH,
    load_player_frames,
    load_crowd_layers,
)
from core.entities.player import Player
from core.entities.ball import Ball
from core.render.court import Court
from core.render.hud import Hud
from core.render.fireworks import spawn_show
from core.iso.projection import world_to_iso
from core.systems.input_controller import read_player_inputs
from core.physics.collisions import ball_vs_player
from core.ai.opponent import ai_drive
from core.audio import sfx
from core.gameplay.players import clamp_player_to_half, reset_players_to_spawn
from core.gameplay.serve import (
    prepare_serve,
    apply_serve_velocity,
    check_point,
    reached_target,
)
from core.utils.paths import asset


class MatchScene:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.hud_font = pygame.font.Font(FONT_PATH, 24)
        self.hud = Hud(self.hud_font)
        self.crowd_layers = load_crowd_layers()
        self.pause_title_font = pygame.font.Font(FONT_PATH, 42)
        self.pause_option_font = pygame.font.Font(FONT_PATH, 28)
        self.pause_options = [
            ("REANUDAR", "resume"),
            ("VOLVER AL MENÚ", "menu"),
            ("SALIR DEL JUEGO", "quit"),
        ]
        self.pause_selection = 0
        self.paused = False
        self._resume_ambient_after_pause = False
        self._resume_festejo_after_pause = False

    def run(self, p2_is_ai: bool):
        court = Court(COURT_BOUNDS, screen_offset=(ISO_OFFSET_X, ISO_OFFSET_Y))
        phys_rect = court.physics_rect
        left_singles_x = court.play_rect.left
        right_singles_x = court.play_rect.right
        blue_frames = load_player_frames("blue")
        red_frames = load_player_frames("red")

        p1 = Player(
            COURT_BOUNDS.left + COURT_BOUNDS.width / 2,
            COURT_BOUNDS.top + COURT_BOUNDS.height * 0.85,
            speed=190,
            is_ai=False,
            name="P1",
            visual_size=(100,100),
            visual_rotation=0.0,
            animation_speed=8.0,
            swing_duration=0.25,
            color=(64, 160, 255),
            sprite_frames=blue_frames,
        )
        p2_speed = 215 if p2_is_ai else 175
        p2 = Player(
            COURT_BOUNDS.left + COURT_BOUNDS.width / 2,
            COURT_BOUNDS.top + COURT_BOUNDS.height * 0.15,
            speed=p2_speed,
            is_ai=p2_is_ai,
            name="P2",
            visual_size=(82,82),
            visual_rotation=0.0,
            animation_speed=8.0,
            swing_duration=0.25,
            color=(220, 70, 70),
            sprite_frames=red_frames,
        )
        ball = Ball(
            COURT_BOUNDS.left + COURT_BOUNDS.width / 2,
            COURT_BOUNDS.top + COURT_BOUNDS.height / 2,
            vx=0,
            vy=0,
            radius=8,
            visual_scale=1.0,
            visual_radius=BALL_VISUAL_RADIUS,
            image_path=asset("ball", "ball.png"),
        )

        server = "P1"
        serve_timer, serve_dir_p2 = prepare_serve(ball, towards_p2=(server == "P1"))
        last_point_scorer = None
        p1_score = 0
        p2_score = 0
        game_over_timer = 0.0
        game_over_winner = None
        fireworks = []

        while True:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sfx.stop_festejo()
                    return "quit"
                pause_decision = self._process_pause_event(event, game_over_timer, game_over_winner)
                if pause_decision in ("menu", "quit"):
                    return pause_decision
                if self.paused:
                    continue

            if not self.paused:
                keys = pygame.key.get_pressed()

                if game_over_timer > 0:
                    game_over_timer = max(0.0, game_over_timer - dt)
                    clamp_player_to_half(p1, top_half=False)
                    clamp_player_to_half(p2, top_half=True)
                    ball.vx = ball.vy = 0.0
                else:
                    if serve_timer > 0:
                        serve_timer -= dt
                        if serve_timer <= 0:
                            apply_serve_velocity(ball, towards_p2=serve_dir_p2)

                serve_locked = (serve_timer > 0) or (game_over_timer > 0)

                if not serve_locked:
                    dx1, dy1 = read_player_inputs(keys, P1_KEYS)
                    p1.apply_input(dx1, dy1, dt)
                    clamp_player_to_half(p1, top_half=False)

                    if not p2.is_ai:
                        dx2, dy2 = read_player_inputs(keys, P2_KEYS)
                        p2.apply_input(dx2, dy2, dt)
                    else:
                        ai_drive(p2, ball, dt)
                    clamp_player_to_half(p2, top_half=True)
                else:
                    clamp_player_to_half(p1, top_half=False)
                    clamp_player_to_half(p2, top_half=True)
                    p1.vx = p1.vy = 0.0
                    p2.vx = p2.vy = 0.0

                ball.update(dt)

                if ball.x - ball.radius < left_singles_x:
                    ball.x = left_singles_x + ball.radius
                    ball.vx *= -1
                elif ball.x + ball.radius > right_singles_x:
                    ball.x = right_singles_x - ball.radius
                    ball.vx *= -1

                last_hitter = ball.last_hitter
                ball_vs_player(ball, p1, phys_rect)
                ball_vs_player(ball, p2, phys_rect)
                if ball.last_hitter != last_hitter:
                    if ball.last_hitter == "P1":
                        p1.trigger_swing()
                    elif ball.last_hitter == "P2":
                        p2.trigger_swing()

                p1.update(dt)
                p2.update(dt)

                p1_score, p2_score, scored, _next_towards_p2, scorer = check_point(ball, p1_score, p2_score)
                if scored:
                    server = scorer
                    reset_players_to_spawn(p1, p2)
                    serve_timer, serve_dir_p2 = prepare_serve(ball, towards_p2=(server == "P1"))
                    last_point_scorer = scorer

                    if reached_target(p1_score, p2_score):
                        game_over_winner = "P1" if p1_score >= TARGET_SCORE else "P2"
                        game_over_timer = 4.5
                        fireworks = spawn_show(SCREEN_W, SCREEN_H, count=28, max_repeats=3)
                        sfx.stop_ambiente()
                        sfx.play_festejo()
                        serve_timer = 0.0
                        ball.vx = ball.vy = 0.0
                        reset_players_to_spawn(p1, p2)
                        if game_over_winner == "P1":
                            p1_score = TARGET_SCORE
                        else:
                            p2_score = TARGET_SCORE

                    if game_over_timer == 0.0 and reached_target(p1_score, p2_score):
                        p1_score = 0
                        p2_score = 0
                        reset_players_to_spawn(p1, p2)
                        server = "P1"
                        serve_timer, serve_dir_p2 = prepare_serve(ball, towards_p2=True)
                        last_point_scorer = None
                        game_over_winner = None

            self._render_scene(
                court,
                [p1, p2, ball],
                fireworks,
                p1_score,
                p2_score,
                serve_timer,
                last_point_scorer,
                game_over_timer,
                game_over_winner,
                p2,
            )
            if self.paused:
                self._draw_pause_menu(selected_index=self.pause_selection)

            pygame.display.flip()

            if not self.paused and game_over_timer > 0 and fireworks:
                for fw in fireworks:
                    fw.update(dt)
                fireworks[:] = [fw for fw in fireworks if not fw.finished]

            if game_over_timer <= 0 and game_over_winner:
                p1_score = 0
                p2_score = 0
                reset_players_to_spawn(p1, p2)
                server = "P1"
                serve_timer, serve_dir_p2 = prepare_serve(ball, towards_p2=True)
                last_point_scorer = None
                game_over_winner = None
                fireworks = []
                sfx.stop_festejo()
                sfx.play_ambiente(restart=True)

    def _render_scene(
        self,
        court,
        entities,
        fireworks,
        p1_score,
        p2_score,
        serve_timer,
        last_point_scorer,
        game_over_timer,
        game_over_winner,
        p2,
    ):
        self.screen.fill(court.fill_color)
        for layer_surface, layer_pos in self.crowd_layers:
            self.screen.blit(layer_surface, layer_pos)
        court.draw(self.screen, world_to_iso)

        entities.sort(key=lambda entity: entity.depth_key())
        for entity in entities:
            entity.draw(self.screen, ISO_OFFSET_X, ISO_OFFSET_Y)

        if game_over_timer > 0 and fireworks:
            for fw in fireworks:
                fw.draw(self.screen)

        self.hud.draw_score(self.screen, p1_score, p2_score, SCREEN_W)

        if serve_timer > 0 and last_point_scorer:
            msg = f"PUNTO PARA {last_point_scorer}"
            color = P1_MSG_COLOR if last_point_scorer == "P1" else P2_MSG_COLOR
            self.hud.draw_center_message(self.screen, msg, color, SCREEN_W, SCREEN_H)

        if game_over_timer > 0 and game_over_winner:
            winner_label = "JUGADOR 1" if game_over_winner == "P1" else "JUGADOR 2"
            color = P1_MSG_COLOR if game_over_winner == "P1" else P2_MSG_COLOR
            self.hud.draw_center_message(
                self.screen,
                f"¡¡¡ GANA EL {winner_label} !!!",
                color,
                SCREEN_W,
                SCREEN_H,
            )

        hint_area_h = 110
        hint_overlay = pygame.Surface((SCREEN_W, hint_area_h), pygame.SRCALPHA)
        hint_overlay.fill((0, 0, 0, 210))
        self.screen.blit(hint_overlay, (0, SCREEN_H - hint_area_h))

        mode_label = "MODO: 1 JUGADOR" if p2.is_ai else "MODO: 2 JUGADORES"
        hint = self.hud_font.render(mode_label + " - ESC para menú", True, (220, 220, 220))
        hint_rect = hint.get_rect()
        hint_rect.left = 24
        hint_rect.centery = SCREEN_H - hint_area_h // 2
        self.screen.blit(hint, hint_rect)

    def _process_pause_event(self, event, game_over_timer, game_over_winner):
        if event.type != pygame.KEYDOWN:
            return False
        if self.paused:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.pause_selection = (self.pause_selection - 1) % len(self.pause_options)
                sfx.play_menu_nav()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.pause_selection = (self.pause_selection + 1) % len(self.pause_options)
                sfx.play_menu_nav()
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                sfx.play_menu_nav()
                return self._handle_pause_action(self.pause_options[self.pause_selection][1])
            elif event.key == pygame.K_ESCAPE:
                sfx.play_menu_nav()
                return self._handle_pause_action("resume")
            return False
        if event.key == pygame.K_ESCAPE:
            self._enter_pause(game_over_timer, game_over_winner)
        return False

    def _enter_pause(self, game_over_timer, game_over_winner):
        if self.paused:
            return
        self.paused = True
        self.pause_selection = 0
        self._resume_ambient_after_pause = game_over_timer <= 0.0
        if self._resume_ambient_after_pause:
            sfx.stop_ambiente()
        self._resume_festejo_after_pause = game_over_timer > 0.0 and game_over_winner is not None
        if self._resume_festejo_after_pause:
            sfx.stop_festejo()

    def _handle_pause_action(self, action):
        if action == "resume":
            self._leave_pause()
            return False
        if action == "menu":
            self.paused = False
            self._resume_ambient_after_pause = False
            self._resume_festejo_after_pause = False
            sfx.stop_festejo()
            return "menu"
        if action == "quit":
            self.paused = False
            self._resume_ambient_after_pause = False
            self._resume_festejo_after_pause = False
            sfx.stop_festejo()
            return "quit"
        return False

    def _leave_pause(self):
        if not self.paused:
            return
        self.paused = False
        if self._resume_ambient_after_pause:
            sfx.play_ambiente(restart=True)
        if self._resume_festejo_after_pause:
            sfx.play_festejo()
        self._resume_ambient_after_pause = False
        self._resume_festejo_after_pause = False

    def _draw_pause_menu(self, selected_index):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        panel_w, panel_h = 640, 320
        panel_surface = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_rect = panel_surface.get_rect()
        pygame.draw.rect(panel_surface, (12, 14, 22, 230), panel_rect, border_radius=20)

        title = self.pause_title_font.render("PAUSA", True, (255, 255, 255))
        panel_surface.blit(title, title.get_rect(center=(panel_w // 2, 72)))

        base_y = 152
        spacing = 62
        for idx, (label, _) in enumerate(self.pause_options):
            row_y = base_y + idx * spacing
            if idx == selected_index:
                highlight_rect = pygame.Rect(36, row_y - 28, panel_w - 72, 56)
                pygame.draw.rect(
                    panel_surface,
                    (70, 130, 220, 160),
                    highlight_rect,
                    border_radius=16,
                )
            color = (255, 255, 255) if idx == selected_index else (200, 200, 200)
            text = self.pause_option_font.render(label, True, color)
            panel_surface.blit(text, text.get_rect(center=(panel_w // 2, row_y)))

        pygame.draw.rect(
            panel_surface,
            (255, 255, 255, 230),
            panel_rect,
            width=2,
            border_radius=20,
        )
        self.screen.blit(
            panel_surface,
            panel_surface.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)),
        )

