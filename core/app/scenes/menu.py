"""Escena de menú principal."""

import pygame

from core.config import BG_COLOR, FPS, SCREEN_W, SCREEN_H
from core.iso.projection import world_to_iso
from core.render.court import Court
from core.entities.player import Player
from core.entities.ball import Ball
from core.app.shared import (
    COURT_BOUNDS,
    ISO_OFFSET_X,
    ISO_OFFSET_Y,
    PLAYER_SPRITE_SIZE,
    BALL_VISUAL_RADIUS,
    FONT_PATH,
    load_player_frames,
)


class MenuScene:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.title_font = pygame.font.Font(FONT_PATH, 56)
        self.option_font = pygame.font.Font(FONT_PATH, 28)
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
                    visual_size=PLAYER_SPRITE_SIZE,
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
                    visual_size=PLAYER_SPRITE_SIZE,
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
                    radius=10,
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
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % len(self.options)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        return self.options[selected][1]
                    elif event.key == pygame.K_ESCAPE:
                        return "exit"

            self.screen.fill(BG_COLOR)
            self.background_court.draw(self.screen, world_to_iso)
            for entity in self.bg_entities:
                entity.update(dt)
                entity.draw(self.screen, ISO_OFFSET_X, ISO_OFFSET_Y)

            self._draw_panel(selected)

            pygame.display.flip()

    def _draw_panel(self, selected_index: int):
        panel_w, panel_h = 480, 320
        panel_surface = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surface.fill((12, 14, 22, 215))

        title = self.title_font.render("TENIS 2D", True, (255, 255, 255))
        panel_surface.blit(title, title.get_rect(center=(panel_w // 2, 72)))

        base_y = 152
        spacing = 62
        for idx, (label, _) in enumerate(self.options):
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
            text = self.option_font.render(label, True, color)
            panel_surface.blit(text, text.get_rect(center=(panel_w // 2, row_y)))

        pygame.draw.rect(
            panel_surface,
            (255, 255, 255, 230),
            panel_surface.get_rect(),
            width=2,
            border_radius=20,
        )
        self.screen.blit(
            panel_surface,
            panel_surface.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)),
        )
