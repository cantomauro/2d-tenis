"""Escena principal del partido."""

import pygame

from core.config import (
    BG_COLOR,
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
    BALL_ANIM_FRAMES,
    BALL_FRAME_DURATION,
    PLAYER_OVERLAY_CONFIG,
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

    def run(self, p2_is_ai: bool):
        court = Court(COURT_BOUNDS, screen_offset=(ISO_OFFSET_X, ISO_OFFSET_Y))
        phys_rect = court.physics_rect
        left_singles_x = court.play_rect.left
        right_singles_x = court.play_rect.right
        blue_assets = PLAYER_OVERLAY_CONFIG["blue"]
        red_assets = PLAYER_OVERLAY_CONFIG["red"]

        p1 = Player(
            COURT_BOUNDS.left + COURT_BOUNDS.width / 2,
            COURT_BOUNDS.top + COURT_BOUNDS.height * 0.85,
            speed=190,
            is_ai=False,
            name="P1",
            visual_size=PLAYER_SPRITE_SIZE,
            visual_rotation=0.0,
            animation_speed=8.0,
            swing_duration=0.25,
            color=(64, 160, 255),
            image_path=blue_assets["body"],
            leg_image_path=blue_assets["leg"],
            hand_image_path=blue_assets["hand"],
            leg_offset=blue_assets["leg_offset"],
            hand_offset=blue_assets["hand_offset"],
            leg_stride=blue_assets["leg_stride"],
            leg_rotation_range=blue_assets["leg_rotation_range"],
            leg_scale=blue_assets["leg_scale"],
            hand_scale=blue_assets["hand_scale"],
        )
        p2_speed = 215 if p2_is_ai else 175
        p2 = Player(
            COURT_BOUNDS.left + COURT_BOUNDS.width / 2,
            COURT_BOUNDS.top + COURT_BOUNDS.height * 0.15,
            speed=p2_speed,
            is_ai=p2_is_ai,
            name="P2",
            visual_size=PLAYER_SPRITE_SIZE,
            visual_rotation=0.0,
            animation_speed=8.0,
            swing_duration=0.25,
            color=(220, 70, 70),
            image_path=red_assets["body"],
            leg_image_path=red_assets["leg"],
            hand_image_path=red_assets["hand"],
            leg_offset=red_assets["leg_offset"],
            hand_offset=red_assets["hand_offset"],
            leg_stride=red_assets["leg_stride"],
            leg_rotation_range=red_assets["leg_rotation_range"],
            leg_scale=red_assets["leg_scale"],
            hand_scale=red_assets["hand_scale"],
        )
        ball = Ball(
            COURT_BOUNDS.left + COURT_BOUNDS.width / 2,
            COURT_BOUNDS.top + COURT_BOUNDS.height / 2,
            vx=0,
            vy=0,
            radius=10,
            visual_scale=1.0,
            visual_radius=BALL_VISUAL_RADIUS,
            image_path=asset("ball", "ball.png"),
            image_frames=BALL_ANIM_FRAMES,
            frame_duration=BALL_FRAME_DURATION,
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sfx.stop_festejo()
                    return "menu"

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
            pygame.display.flip()

            if game_over_timer > 0 and fireworks:
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
        self.screen.fill(BG_COLOR)
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

        mode_label = "MODO: 1 JUGADOR" if p2.is_ai else "MODO: 2 JUGADORES"
        hint = self.hud_font.render(mode_label + " - ESC para menú", True, (200, 200, 200))
        self.screen.blit(hint, (16, SCREEN_H - 48))
