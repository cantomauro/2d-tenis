import pygame

class Court:
    def __init__(self, world_rect, screen_offset=(0, 0)):
        self.world_rect = world_rect
        self.ox, self.oy = screen_offset

    def draw(self, surface, world_to_iso):
        # Dibujo isométrico básico: 4 esquinas del rect mundo -> iso, luego un polígono
        l, t, w, h = self.world_rect
        r, b = l + w, t + h
        corners = [(l, t), (r, t), (r, b), (l, b)]
        iso_pts = [world_to_iso(x, y, self.ox, self.oy) for (x, y) in corners]
        pygame.draw.polygon(surface, (30, 120, 60), iso_pts, width=0)
        pygame.draw.polygon(surface, (255, 255, 255), iso_pts, width=2)
