import pygame


def draw_menu_panel(
    surface: pygame.Surface,
    title_font: pygame.font.Font,
    option_font: pygame.font.Font,
    title: str,
    options: list[tuple[str, str]],
    selected_index: int,
    center: tuple[int, int],
    *,
    panel_size: tuple[int, int] = (640, 320),
    background_color=(12, 14, 22, 215),
    highlight_color=(70, 130, 220, 160),
    border_color=(255, 255, 255, 230),
    title_y=72,
    base_y=152,
    spacing=62,
) -> None:
    """Renderiza un panel de opciones estilizado como el menú principal."""

    panel_surface = pygame.Surface(panel_size, pygame.SRCALPHA)
    panel_rect = panel_surface.get_rect()

    pygame.draw.rect(panel_surface, background_color, panel_rect, border_radius=20)

    title_surf = title_font.render(title, True, (255, 255, 255))
    panel_surface.blit(title_surf, title_surf.get_rect(center=(panel_rect.width // 2, title_y)))

    for idx, (label, _) in enumerate(options):
        row_y = base_y + idx * spacing
        if idx == selected_index:
            highlight_rect = pygame.Rect(36, row_y - 28, panel_rect.width - 72, 56)
            pygame.draw.rect(
                panel_surface,
                highlight_color,
                highlight_rect,
                border_radius=16,
            )
        color = (255, 255, 255) if idx == selected_index else (200, 200, 200)
        text = option_font.render(label, True, color)
        panel_surface.blit(text, text.get_rect(center=(panel_rect.width // 2, row_y)))

    pygame.draw.rect(
        panel_surface,
        border_color,
        panel_rect,
        width=2,
        border_radius=20,
    )

    surface.blit(panel_surface, panel_surface.get_rect(center=center))
