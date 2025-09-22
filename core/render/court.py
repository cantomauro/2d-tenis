# core/render/court.py
import pygame

class Court:
    def __init__(self, world_rect: pygame.Rect, screen_offset=(0, 0),
                 fill_color=(30, 120, 60), line_color=(255, 255, 255)):
        self.net_color = (229, 190, 1)
        self.world_rect = world_rect           # borde exterior (paredes)
        self.physics_rect = world_rect.copy()  # alias explícito para física
        self.ox, self.oy = screen_offset
        self.fill_color = fill_color
        self.line_color = line_color

        # ---- Cálculos geométricos base (una sola vez) ----
        l, t, r, b = world_rect.left, world_rect.top, world_rect.right, world_rect.bottom
        w, h = r - l, b - t
        self.cx = (l + r) / 2.0
        self.cy = (t + b) / 2.0

        # laterales de singles
        singles_ratio = 8.23 / 10.97
        inset = (1.0 - singles_ratio) / 2.0 * w  # float

        # Redondeo simétrico a enteros para evitar desfasajes por truncado
        self.x_left_singles = int(round(l + inset))
        self.x_right_singles = int(round(r - inset))

        # Rect de juego (singles) construido con esos enteros
        self.play_rect = pygame.Rect(
            self.x_left_singles,
            t,
            self.x_right_singles - self.x_left_singles,
            h
        )

        # líneas de saque
        service_offset = (6.40 / 23.77) * h
        self.service_y_top = self.cy - service_offset
        self.service_y_bot = self.cy + service_offset

        # marca central (muesca) = 0.10m
        self.center_mark_h = (0.10 / 23.77) * h

    def iso_corners(self, world_to_iso_fn):
        l, t, r, b = self.world_rect.left, self.world_rect.top, self.world_rect.right, self.world_rect.bottom
        corners = [(l, t), (r, t), (r, b), (l, b)]
        return [world_to_iso_fn(x, y, self.ox, self.oy) for (x, y) in corners]

    def draw(self, surface, world_to_iso_fn):
        # piso + contorno exterior
        pts = self.iso_corners(world_to_iso_fn)
        pygame.draw.polygon(surface, self.fill_color, pts, 0)
        pygame.draw.polygon(surface, self.line_color, pts, 2)

        def P(x, y):
            sx, sy = world_to_iso_fn(x, y, self.ox, self.oy)
            return int(sx), int(sy)

        def draw_world_line(x1, y1, x2, y2, color, width):
            pygame.draw.line(surface, color, P(x1, y1), P(x2, y2), width)

        l, t, r, b = self.world_rect.left, self.world_rect.top, self.world_rect.right, self.world_rect.bottom

        # red
        draw_world_line(l, self.cy, r, self.cy, self.net_color, 3)

        # laterales singles
        draw_world_line(self.x_left_singles, t, self.x_left_singles, b, self.line_color, 2)
        draw_world_line(self.x_right_singles, t, self.x_right_singles, b, self.line_color, 2)

        # líneas de saque
        draw_world_line(self.x_left_singles, self.service_y_top, self.x_right_singles, self.service_y_top, self.line_color, 2)
        draw_world_line(self.x_left_singles, self.service_y_bot, self.x_right_singles, self.service_y_bot, self.line_color, 2)

        # línea central de servicio
        draw_world_line(self.cx, self.service_y_top, self.cx, self.service_y_bot, self.line_color, 2)

        # muescas centrales en fondos
        draw_world_line(self.cx, t, self.cx, t + self.center_mark_h, self.line_color, 2)
        draw_world_line(self.cx, b, self.cx, b - self.center_mark_h, self.line_color, 2)
