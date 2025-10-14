
class Hud:
    def __init__(self, font):
        self.font = font

    def draw_score(self, surface, p1_score, p2_score, screen_w):
        text = self.font.render(f"{p1_score}  -  {p2_score}", True, (255,255,255))
        rect = text.get_rect(center=(screen_w//2, 24))
        surface.blit(text, rect)

    # mensaje centrado para que se lea siempre
    def draw_center_message(self, surface, text, color, screen_w, screen_h):
        x, y = screen_w // 2, screen_h // 2
        txt = self.font.render(text, True, color)
        shadow = self.font.render(text, True, (0, 0, 0))
        for dx, dy in ((1,1), (-1,1), (1,-1), (-1,-1)):
            surface.blit(shadow, shadow.get_rect(center=(x + dx, y + dy)))
        surface.blit(txt, txt.get_rect(center=(x, y)))
