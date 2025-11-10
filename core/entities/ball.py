# core/entities/ball.py
import pygame
from core.entities.base import Entity
from core.utils.paths import asset


class Ball(Entity):
    def __init__(
        self,
        x,
        y,
        vx=220,
        vy=-160,
        radius=1,
        image_path=None,
        image_frames=None,
        frame_duration=0.15,
        visual_scale=1.0,
        visual_radius=None,
    ):
        super().__init__(x, y)
        self.vx, self.vy = vx, vy
        self.radius = radius              # ← tamaño de colisión
        self.visual_scale = float(visual_scale)  # ← multiplicador visual (1.0 = igual que radius)
        self.visual_radius = visual_radius  # ← override absoluto visual en “radio”
        self.last_hitter = None    # "P1" | "P2" | None
        self.hit_cooldown = 0.0    # segundos restantes de cooldown
        self._img = None
        self._img_scaled = None
        self._img_scale_key = None
        try:
            if image_frames:
                self._frames_original = [
                    pygame.image.load(frame).convert_alpha() for frame in image_frames
                ]
            else:
                if image_path is None:
                    image_path = asset("ball", "ball.png")
                self._img = pygame.image.load(image_path).convert_alpha()
                self._frames_original = []
        except Exception:
            self._img = None
            self._frames_original = []
        self._use_frames = len(self._frames_original) > 0
        self._frame_duration = float(frame_duration)
        self._frame_timer = 0.0
        self._frame_index = 0
        self._frames_cache = {}

    @property
    def hit_circle(self):
        return (self.x, self.y, self.radius)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.hit_cooldown > 0:
            self.hit_cooldown = max(0.0, self.hit_cooldown - dt)
        if self._use_frames and self._frame_duration > 0 and self._frames_original:
            self._frame_timer += dt
            while self._frame_timer >= self._frame_duration:
                self._frame_timer -= self._frame_duration
                self._frame_index = (self._frame_index + 1) % len(self._frames_original)

    def _get_scaled_image(self):
        if self._use_frames:
            return self._get_current_frame()
        if not self._img:
            return None
        # base visual: visual_radius (si está) o radius
        base_r = self.visual_radius if self.visual_radius is not None else self.radius
        target = max(4, int(base_r * 2 * self.visual_scale))
        if self._img_scale_key != target:
            self._img_scaled = pygame.transform.smoothscale(self._img, (target, target))
            self._img_scale_key = target
        return self._img_scaled

    def _get_current_frame(self):
        if not self._frames_original:
            return None
        base = self._frames_original[self._frame_index % len(self._frames_original)]
        base_r = self.visual_radius if self.visual_radius is not None else self.radius
        target = max(4, int(base_r * 2 * self.visual_scale))
        key = (self._frame_index, target)
        cached = self._frames_cache.get(key)
        if cached:
            return cached
        scaled = pygame.transform.smoothscale(base, (target, target))
        self._frames_cache[key] = scaled
        return scaled

    def draw(self, surface, ox=0, oy=0):
        sx, sy = self.screen_pos(ox, oy)
        img = self._get_scaled_image()
        if img:
            rect = img.get_rect(center=(int(sx), int(sy)))
            surface.blit(img, rect)
        else:
            pygame.draw.circle(surface, (250,220,80), (int(sx), int(sy)), max(2, int(self.radius*0.9)))

    def set_velocity_dir(self, speed, dir_x, dir_y):
        # Normaliza (dir_x, dir_y) y aplica 'speed' manteniendo dirección
        import math
        mag = math.hypot(dir_x, dir_y)
        if mag < 1e-6:
            return  # evita división por cero
        self.vx = speed * (dir_x / mag)
        self.vy = speed * (dir_y / mag)
