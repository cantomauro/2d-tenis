import pygame
from core.entities.base import Entity

class Ball(Entity):
    def __init__(self, x, y, vx=220, vy=-160, radius=1, image_path="core/entities/ball.png",
                 visual_scale=1.0, visual_radius=None):
        super().__init__(x, y)
        self.vx, self.vy = vx, vy
        self.radius = radius # tamaño de colisión
        self.visual_scale = 1  # multiplicador visual (1.0 = igual que radius)
        self.visual_radius = visual_radius
        self.last_hitter = None    # p1. p2 o ninguno
        self.hit_cooldown = 0.0    # segundos restantes de cooldown
        self._img = None
        self._img_scaled = None
        self._img_scale_key = None
        try:
            self._img = pygame.image.load(image_path).convert_alpha()
        except Exception:
            self._img = None

    @property
    def hit_circle(self):
        return (self.x, self.y, self.radius)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.hit_cooldown > 0:
            self.hit_cooldown = max(0.0, self.hit_cooldown - dt)

    def _get_scaled_image(self):
        if not self._img:
            return None
        # base visual: visual_radius o radius
        base_r = self.visual_radius if self.visual_radius is not None else self.radius
        target = max(4, int(self.radius * 2 * self.visual_scale))
        if self._img_scale_key != target:
            self._img_scaled = pygame.transform.smoothscale(self._img, (target, target))
            self._img_scale_key = target
        return self._img_scaled

    def draw(self, surface, ox=0, oy=0):
        sx, sy = self.screen_pos(ox, oy)
        img = self._get_scaled_image()
        if img:
            rect = img.get_rect(center=(int(sx), int(sy)))
            surface.blit(img, rect)
        else:
            pygame.draw.circle(surface, (250,220,80), (int(sx), int(sy)), max(2, int(self.radius*0.9)))

    def set_velocity_dir(self, speed, dir_x, dir_y):
        # normaliza (dir_x, dir_y) y aplica 'la velocidad manteniendo dirección
        import math
        mag = math.hypot(dir_x, dir_y)
        if mag < 1e-6:
            return  # evita división por cero
        self.vx = speed * (dir_x / mag)
        self.vy = speed * (dir_y / mag)