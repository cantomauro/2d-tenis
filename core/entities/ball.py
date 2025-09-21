# clase Ball (pos, vel, radio), reinicio, avance, devuelve su hit_circle.

import pygame
from core.entities.base import Entity

class Ball(Entity):
    def __init__(self, x, y, vx=220, vy=-160, radius=6):
        super().__init__(x, y)
        self.vx, self.vy = vx, vy
        self.radius = radius
        self.color = (250, 220, 80)

    @property
    def hit_circle(self):
        return self.x, self.y, self.radius

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface, ox=0, oy=0):
        sx, sy = self.screen_pos(ox, oy)
        pygame.draw.circle(surface, self.color, (int(sx), int(sy)), max(2, int(self.radius*0.9)))
