# core/render/court.py
import pygame

class Court:

    def __init__(self, world_rect: pygame.Rect, screen_offset=(0, 0),
        fill_color=(30, 120, 60), line_color=(255, 255, 255)):
        self.net_color = (229, 190, 1)
        self.world_rect = world_rect
        self.ox, self.oy = screen_offset
        self.fill_color = fill_color
        self.line_color = line_color

    def iso_corners(self, world_to_iso_fn):
# Convierte las 4 esquinas del rectángulo de mundo a puntos isométricos.
# Orden: topleft -> topright -> bottomright -> bottomleft
        l = self.world_rect.left
        t = self.world_rect.top
        r = self.world_rect.right
        b = self.world_rect.bottom
        corners = [(l, t), (r, t), (r, b), (l, b)]
        return [world_to_iso_fn(x, y, self.ox, self.oy) for (x, y) in corners]

    def draw(self, surface, world_to_iso_fn):
        # piso y contorno de la cancha (polígono isométrico)
        pts = self.iso_corners(world_to_iso_fn)
        pygame.draw.polygon(surface, self.fill_color, pts, 0)
        pygame.draw.polygon(surface, self.line_color, pts, 2)

        # helpers locales para dibujar líneas
        def P(x, y):
            sx, sy = world_to_iso_fn(x, y, self.ox, self.oy)
            return int(sx), int(sy)

        def draw_world_line(x1, y1, x2, y2, color, width):
            pygame.draw.line(surface, color, P(x1, y1), P(x2, y2), width)

        # datos básicos del rectángulo de la cancha
        l = self.world_rect.left
        t = self.world_rect.top
        r = self.world_rect.right
        b = self.world_rect.bottom
        w = r - l
        h = b - t
        cx = (l + r) / 2.0  # centro X (verticales centrales)
        cy = (t + b) / 2.0  # centro Y (posición de la red)

        # red (línea horizontal en el centro)
        draw_world_line(l, cy, r, cy, self.net_color, 3)

        # líneas de singles (laterales internas)
        singles_ratio = 8.23 / 10.97
        inset = (1.0 - singles_ratio) / 2.0 * w  # cuánto entrar desde cada lateral
        x_left_singles = l + inset
        x_right_singles = r - inset
        draw_world_line(x_left_singles, t, x_left_singles, b, self.line_color, 2)
        draw_world_line(x_right_singles, t, x_right_singles, b, self.line_color, 2)

        # líneas de saque (paralelas al fondo) a 6.40 m de la red en cada lado
        service_offset = (6.40 / 23.77) * h
        y_service_top = cy - service_offset
        y_service_bot = cy + service_offset
        draw_world_line(x_left_singles, y_service_top, x_right_singles, y_service_top, self.line_color, 2)
        draw_world_line(x_left_singles, y_service_bot, x_right_singles, y_service_bot, self.line_color, 2)

        # línea central de servicio (vertical) entre las dos líneas de servicio
        draw_world_line(cx, y_service_top, cx, y_service_bot, self.line_color, 2)

        # marcas centrales en las líneas de fondo (pequeñas “muescas” de 0.10 m)
        center_mark = (0.10 / 23.77) * h
        draw_world_line(cx, t, cx, t + center_mark, self.line_color, 2)  # arriba
        draw_world_line(cx, b, cx, b - center_mark, self.line_color, 2)  # abajo
