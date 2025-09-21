# clase Player (humano o IA con flag), hit_rect, velocidad, estado de animación/dirección.

import pygame
from core.entities.base import Entity

PLAYER_W, PLAYER_H = 28, 18  # hitbox de colisión (mundo)

class Player(Entity):
    def __init__(self, x, y, speed=180, is_ai=False, name="P"):
        super().__init__(x, y)
        self.speed = speed
        self.is_ai = is_ai
        self.name = name
        self.vx = 0; self.vy = 0
        self.color = (40, 160, 255)

    @property
    def hit_rect(self):  # rect en MUNDO
        return pygame.Rect(int(self.x - PLAYER_W/2), int(self.y - PLAYER_H/2), PLAYER_W, PLAYER_H)

    def apply_input(self, dx, dy, dt):
        self.vx = dx * self.speed
        self.vy = dy * self.speed
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface, ox=0, oy=0):
        sx, sy = self.screen_pos(ox, oy)
        # Representación temporal: el hitbox como rect isométrico aproximado
        pygame.draw.rect(surface, self.color, (sx-8, sy-6, 16, 12), width=0)
