"""Escena de menú principal."""

import pygame

from core.config import FPS, SCREEN_W, SCREEN_H
from core.iso.projection import world_to_iso
from core.render.court import Court
from core.entities.player import Player
from core.entities.ball import Ball
from core.audio import sfx
from core.app.shared import (
    COURT_BOUNDS,
    ISO_OFFSET_X,
    ISO_OFFSET_Y,
    BALL_VISUAL_RADIUS,
    FONT_PATH,
    load_player_frames,
    load_crowd_layers,
)
from core.ui.menu_panel import draw_menu_panel


class MenuScene:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.title_font = pygame.font.Font(FONT_PATH, 42)
        self.option_font = pygame.font.Font(FONT_PATH, 28)
        self.crowd_layers = load_crowd_layers()
        self.options = [
            ("1 JUGADOR (VS IA)", "solo"),
            ("2 JUGADORES", "versus"),
            ("SALIR", "exit"),
        ]
        self.background_court = Court(COURT_BOUNDS, screen_offset=(ISO_OFFSET_X, ISO_OFFSET_Y))
        blue_frames = load_player_frames("blue")
        red_frames = load_player_frames("red")
        self.bg_entities = sorted(
            [
                Player(
                    COURT_BOUNDS.left + COURT_BOUNDS.width / 2,
                    COURT_BOUNDS.top + COURT_BOUNDS.height * 0.82,
                    speed=0,
                    is_ai=False,
                    name="P1",
                    visual_size=(100, 100),
                    visual_rotation=0.0,
                    color=(64, 160, 255),
                    sprite_frames=blue_frames,
                    animation_speed=6.0,
                    swing_duration=0.25,
                ),
                Player(
                    COURT_BOUNDS.left + COURT_BOUNDS.width / 2,
                    COURT_BOUNDS.top + COURT_BOUNDS.height * 0.18,
                    speed=0,
                    is_ai=True,
                    name="P2",
                    visual_size=(82, 82),
                    visual_rotation=0.0,
                    color=(220, 70, 70),
                    sprite_frames=red_frames,
                    animation_speed=6.0,
                    swing_duration=0.25,
                ),
                Ball(
                    COURT_BOUNDS.left + COURT_BOUNDS.width / 2,
                    COURT_BOUNDS.top + COURT_BOUNDS.height / 2,
                    vx=0,
                    vy=0,
                    radius=8,
                    visual_scale=1.0,
                    visual_radius=BALL_VISUAL_RADIUS,
                ),
            ],
            key=lambda e: e.depth_key(),
        )

    def run(self):
        selected = 0
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected = (selected - 1) % len(self.options)
                        sfx.play_menu_nav()
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % len(self.options)
                        sfx.play_menu_nav()
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        sfx.play_menu_nav()
                        return self.options[selected][1]
                    elif event.key == pygame.K_ESCAPE:
                        sfx.play_menu_nav()
                        return "exit"

            self.screen.fill(self.background_court.fill_color)
            for layer_surface, layer_pos in self.crowd_layers:
                self.screen.blit(layer_surface, layer_pos)
            self.background_court.draw(self.screen, world_to_iso)
            for entity in self.bg_entities:
                entity.update(dt)
                entity.draw(self.screen, ISO_OFFSET_X, ISO_OFFSET_Y)

            self._draw_panel(selected)

            pygame.display.flip()

    def _draw_panel(self, selected_index: int):
        draw_menu_panel(
            self.screen,
            self.title_font,
            self.option_font,
            "ARKANOID TENIS",
            self.options,
            selected_index,
            center=(SCREEN_W // 2, SCREEN_H // 2),
        )
