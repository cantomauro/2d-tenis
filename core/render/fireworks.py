import random
import pygame

from core.utils.paths import asset

_SPRITES_CACHE = {}


def _load_frames(sprite_name, frame_w=40, frame_h=40):
    cache_key = (sprite_name, frame_w, frame_h)
    if cache_key in _SPRITES_CACHE:
        return _SPRITES_CACHE[cache_key]

    path = asset("fireworks", sprite_name + ".png")
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    total = sheet.get_width() // frame_w
    for idx in range(total):
        rect = pygame.Rect(idx * frame_w, 0, frame_w, frame_h)
        frames.append(sheet.subsurface(rect).copy())
    _SPRITES_CACHE[cache_key] = frames
    return frames


class Firework:
    def __init__(self, color, position, scale=1.0, speed=14.0, repeats=2):
        frames = _load_frames(color)
        self.frames = frames
        self.position = position
        self.scale = scale
        self.speed = speed
        self.time = 0.0
        self.finished = False
        self.repeats = 0
        self.max_repeats = repeats

    def update(self, dt):
        if self.finished:
            return
        self.time += dt * self.speed
        if self.time >= len(self.frames):
            self.repeats += 1
            if self.repeats >= self.max_repeats:
                self.finished = True
            else:
                self.time = 0.0

    def draw(self, surface):
        if self.finished:
            return
        frame_index = int(self.time)
        frame_index = min(frame_index, len(self.frames) - 1)
        frame = self.frames[frame_index]
        if self.scale != 1.0:
            size = (
                max(1, int(frame.get_width() * self.scale)),
                max(1, int(frame.get_height() * self.scale)),
            )
            frame = pygame.transform.smoothscale(frame, size)
        rect = frame.get_rect(center=self.position)
        surface.blit(frame, rect)


def spawn_show(screen_w, screen_h, count=20, max_repeats=3):
    colors = ["redshot", "blueshot", "yellowshot", "violetshot"]
    fireworks = []
    for _ in range(count):
        color = random.choice(colors)
        x = random.randint(screen_w // 10, screen_w - screen_w // 10)
        y = random.randint(screen_h // 8, screen_h - screen_h // 3)
        scale = random.uniform(2.0, 3.4)
        speed = random.uniform(9.0, 14.0)
        repeats = random.randint(2, max_repeats)
        fireworks.append(Firework(color, (x, y), scale=scale, speed=speed, repeats=repeats))
    return fireworks
