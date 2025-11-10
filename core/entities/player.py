# core/entities/player.py
from __future__ import annotations

import pygame

from core.entities.base import Entity

PLAYER_W, PLAYER_H = 28, 18  # hitbox de colisión (mundo)


class Player(Entity):
    def __init__(
        self,
        x,
        y,
        speed=180,
        is_ai=False,
        name="P",
        image_path=None,
        visual_scale=1.0,
        visual_size=None,
        visual_rotation=0.0,
        sprite_frames=None,
        animation_speed=6.0,
        swing_duration=0.18,
        color=(40, 160, 255),
        leg_image_path=None,
        hand_image_path=None,
        leg_offset=(0, 8),
        hand_offset=(2, -6),
        leg_stride=3.0,
        leg_cycle_duration=0.5,
        leg_rotation_range=(-12.0, 12.0),
        leg_scale=0.65,
        hand_scale=0.45,
    ):
        """
        visual_scale: escala relativa del sprite respecto al hitbox (si visual_size es None)
        visual_size:  (w, h) tamaño absoluto del sprite (opcional). Si se define ignora visual_scale.
        """
        super().__init__(x, y)
        self.speed = speed
        self.is_ai = is_ai
        self.name = name
        self.vx = 0.0
        self.vy = 0.0
        self.color = color

        self.visual_scale = float(visual_scale)
        self.visual_size = visual_size
        self.visual_rotation = float(visual_rotation)
        self.home_x = x
        self.home_y = y
        self._use_frames = bool(sprite_frames)
        self._frames_original = [frame.copy() for frame in sprite_frames] if sprite_frames else []
        self._frames_cache: dict[tuple, pygame.Surface] = {}
        self._animation_speed = float(animation_speed)
        self._swing_duration = float(swing_duration)
        self._anim_timer = 0.0
        self._move_cycle = [0, 1] if len(self._frames_original) > 1 else [0]
        self._anim_index = self._move_cycle[0] if self._move_cycle else 0
        self._swing_timer = 0.0
        self._moving = False
        self._swing_frame = 2 if len(self._frames_original) > 2 else (self._move_cycle[-1])

        self._img = None
        self._img_scaled = None
        self._img_scale_key = None
        if not self._use_frames and image_path:
            try:
                self._img = pygame.image.load(image_path).convert_alpha()
            except Exception as e:
                print(f"[Player] No pude cargar imagen '{image_path}': {e}")
                self._img = None
        self._leg_image = self._load_overlay_image(leg_image_path)
        self._hand_image = self._load_overlay_image(hand_image_path)
        self._leg_offset = tuple(leg_offset)
        self._hand_offset = tuple(hand_offset)
        self._leg_stride = float(leg_stride)
        self._leg_cycle_duration = max(1e-3, float(leg_cycle_duration))
        min_angle, max_angle = leg_rotation_range
        self._leg_rotation_range = (float(min_angle), float(max_angle))
        self._leg_scale = float(leg_scale)
        self._hand_scale = float(hand_scale)
        self._leg_timer = 0.0
        self._leg_phase = 0
        self._overlay_cache: dict[tuple, pygame.Surface] = {}

    @property
    def hit_rect(self):
        return pygame.Rect(int(self.x - PLAYER_W / 2), int(self.y - PLAYER_H / 2), PLAYER_W, PLAYER_H)

    def apply_input(self, dx, dy, dt):
        self.vx = dx * self.speed
        self.vy = dy * self.speed
        self.x += self.vx * dt
        self.y += self.vy * dt
        self._moving = (dx != 0 or dy != 0)

    def _get_scaled_image(self):
        return self._get_body_image()

    def _get_body_image(self):
        if self._use_frames:
            return self._get_current_frame()
        return self._get_static_image()

    def _get_static_image(self):
        if not self._img:
            return None
        target_size = self._get_visual_target_size()
        rotation = round(self.visual_rotation, 3)
        key = ("body", tuple(target_size), rotation)
        if self._img_scale_key == key:
            return self._img_scaled
        scaled = pygame.transform.smoothscale(self._img, target_size)
        if rotation:
            scaled = pygame.transform.rotate(scaled, rotation)
        self._img_scaled = scaled
        self._img_scale_key = key
        return scaled

    def _get_current_frame(self):
        if not self._frames_original:
            return None

        if self._swing_timer > 0:
            frame_idx = self._swing_frame
        else:
            frame_idx = self._anim_index if self._move_cycle else 0

        base = self._frames_original[frame_idx % len(self._frames_original)]
        rotation = round(self.visual_rotation, 3)
        target_size = self._get_visual_target_size()
        key = (frame_idx, tuple(target_size), round(self.visual_scale, 3), rotation)
        cached = self._frames_cache.get(key)
        if cached:
            return cached

        image = pygame.transform.scale(base, target_size)
        if rotation:
            image = pygame.transform.rotate(image, rotation)
        self._frames_cache[key] = image
        return image

    def _get_visual_target_size(self):
        if self.visual_size:
            try:
                return tuple(self.visual_size)
            except (TypeError, ValueError):
                pass
        target_w = max(8, int(PLAYER_W * self.visual_scale))
        target_h = max(8, int(PLAYER_H * self.visual_scale * 1.2))
        return (target_w, target_h)

    def trigger_swing(self):
        if not self._use_frames:
            return
        self._swing_timer = self._swing_duration

    def update(self, dt):
        self._moving = abs(self.vx) > 1e-3 or abs(self.vy) > 1e-3
        self._update_leg_cycle(dt)
        if not self._use_frames:
            return
        if self._swing_timer > 0:
            self._swing_timer = max(0.0, self._swing_timer - dt)
            if self._swing_timer == 0:
                self._anim_index = 0
                self._anim_timer = 0.0
            return

        if self._moving and len(self._move_cycle) > 1:
            if self._anim_index not in self._move_cycle:
                self._anim_index = self._move_cycle[0]
            self._anim_timer += dt
            frame_time = 1.0 / max(1.0, self._animation_speed)
            if self._anim_timer >= frame_time:
                self._anim_timer -= frame_time
                current = self._move_cycle.index(self._anim_index) if self._anim_index in self._move_cycle else 0
                self._anim_index = self._move_cycle[(current + 1) % len(self._move_cycle)]
        else:
            self._anim_index = self._move_cycle[0]
            self._anim_timer = 0.0

    def draw(self, surface, ox=0, oy=0):
        sx, sy = self.screen_pos(ox, oy)
        center_x, center_y = int(sx), int(sy)
        self._draw_leg(surface, center_x, center_y)
        img = self._get_scaled_image()
        if img:
            rect = img.get_rect(center=(center_x, center_y))
            surface.blit(img, rect)
        else:
            size = self.visual_size or (16, 16)
            try:
                rect_w, rect_h = int(size[0]), int(size[1])
            except (TypeError, IndexError):
                rect_w = rect_h = 16
            rect = pygame.Rect(0, 0, rect_w, rect_h)
            rect.center = (center_x, center_y)
            pygame.draw.rect(surface, self.color, rect)
        self._draw_hand(surface, center_x, center_y)

    def _update_leg_cycle(self, dt):
        if not self._leg_image:
            return
        if not self._moving:
            self._leg_timer = 0.0
            self._leg_phase = 0
            return
        phase_interval = max(1e-3, self._leg_cycle_duration / 2.0)
        self._leg_timer += dt
        while self._leg_timer >= phase_interval:
            self._leg_timer -= phase_interval
            self._leg_phase = 1 - self._leg_phase

    def _get_leg_image(self):
        if not self._leg_image:
            return None
        angle = self._leg_rotation_range[0] if self._leg_phase == 0 else self._leg_rotation_range[1]
        return self._get_scaled_overlay(self._leg_image, self._leg_scale, angle)

    def _draw_leg(self, surface, center_x, center_y):
        leg = self._get_leg_image()
        if not leg:
            return
        stride_dir = 0 if not self._moving else (-1 if self._leg_phase == 0 else 1)
        offset_x = self._leg_offset[0] + stride_dir * self._leg_stride
        offset_y = self._leg_offset[1]
        rect = leg.get_rect(center=(int(center_x + offset_x), int(center_y + offset_y)))
        surface.blit(leg, rect)

    def _draw_hand(self, surface, center_x, center_y):
        hand = self._get_scaled_overlay(self._hand_image, self._hand_scale, 0.0)
        if not hand:
            return
        offset_x, offset_y = self._hand_offset
        rect = hand.get_rect(center=(int(center_x + offset_x), int(center_y + offset_y)))
        surface.blit(hand, rect)

    def _get_scaled_overlay(self, overlay, scale, rotation):
        if not overlay:
            return None
        base_size = self._get_visual_target_size()
        target_w = max(1, int(base_size[0] * scale))
        target_h = max(1, int(base_size[1] * scale))
        key = (id(overlay), target_w, target_h, round(rotation, 3))
        cached = self._overlay_cache.get(key)
        if cached:
            return cached
        scaled = pygame.transform.smoothscale(overlay, (target_w, target_h))
        if rotation:
            scaled = pygame.transform.rotate(scaled, rotation)
        self._overlay_cache[key] = scaled
        return scaled

    def _load_overlay_image(self, path):
        if not path:
            return None
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception as exc:
            print(f"[Player] No pude cargar overlay '{path}': {exc}")
            return None
