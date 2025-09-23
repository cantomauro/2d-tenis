# core/entities/player.py
import pygame
from core.entities.base import Entity

PLAYER_W, PLAYER_H = 28, 18  # hitbox de colisión (mundo)

class Player(Entity):
    def __init__(self, x, y, speed=180, is_ai=False, name="P",
                 image_path=None, visual_scale=1.0, visual_size=None):
        """
        visual_scale: escala relativa del sprite respecto al hitbox (si visual_size es None)
        visual_size:  (w, h) tamaño absoluto del sprite (opcional). Si se define, ignora visual_scale.
        """
        super().__init__(x, y)
        self.speed = speed
        self.is_ai = is_ai
        self.name = name
        self.vx = 0.0
        self.vy = 0.0
        self.color = (40, 160, 255)

        # >>> FIX: estos vienen de la firma
        self.visual_scale = float(visual_scale)
        self.visual_size  = visual_size  # None o (w, h)

        # Imagen
        if image_path is None:
            # Usa assets/player/player.png por defecto
            image_path = "core/entities/player.png"
        self._img = None
        self._img_scaled = None
        self._img_scale_key = None
        try:
            self._img = pygame.image.load(image_path).convert_alpha()
        except Exception as e:
            print(f"[Player] No pude cargar imagen '{image_path}': {e}")
            self._img = None

    @property
    def hit_rect(self):  # rect en MUNDO
        return pygame.Rect(int(self.x - PLAYER_W/2), int(self.y - PLAYER_H/2), PLAYER_W, PLAYER_H)

    def apply_input(self, dx, dy, dt):
        self.vx = dx * self.speed
        self.vy = dy * self.speed
        self.x += self.vx * dt
        self.y += self.vy * dt

    def _get_scaled_image(self):
        if not self._img:
            return None

        # Si se da tamaño absoluto, lo usamos
        if self.visual_size:
            key = ("abs", tuple(self.visual_size))
            if self._img_scale_key != key:
                self._img_scaled = pygame.transform.smoothscale(self._img, self.visual_size)
                self._img_scale_key = key
            return self._img_scaled

        # Si no, escalamos relativo al hitbox
        target_w = max(8, int(PLAYER_W * self.visual_scale))
        target_h = max(8, int(PLAYER_H * self.visual_scale * 1.2))
        key = ("rel", target_w, target_h)
        if self._img_scale_key != key:
            self._img_scaled = pygame.transform.smoothscale(self._img, (target_w, target_h))
            self._img_scale_key = key
        return self._img_scaled

    def draw(self, surface, ox=0, oy=0):
        sx, sy = self.screen_pos(ox, oy)
        img = self._get_scaled_image()
        if img:
            rect = img.get_rect(center=(int(sx), int(sy)))
            surface.blit(img, rect)
        else:
            # Fallback si no hay imagen
            pygame.draw.rect(surface, self.color, (sx-8, sy-6, 16, 12), width=0)
