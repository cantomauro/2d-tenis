"""Punto de entrada del juego: orquesta escenas y ciclo principal."""

import sys
import pygame

from core.config import SCREEN_SIZE, WINDOW_ICON_SCALE
from core.app.scenes import MenuScene, MatchScene
from core.audio import sfx
from core.utils.paths import asset


class GameEngine:
    def __init__(self):
        self.screen = None
        self.clock = None
        self.running = True
        self.menu_scene = None
        self.match_scene = None

    def initialise(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        pygame.display.set_caption("ARKANOID TENIS")
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        icon_path = asset("logo", "logo.png")
        try:
            icon_surface = pygame.image.load(icon_path).convert_alpha()
            if WINDOW_ICON_SCALE != 1.0:
                width, height = icon_surface.get_size()
                scaled_size = (
                    max(1, int(width * WINDOW_ICON_SCALE)),
                    max(1, int(height * WINDOW_ICON_SCALE)),
                )
                icon_surface = pygame.transform.smoothscale(icon_surface, scaled_size)
            pygame.display.set_icon(icon_surface)
        except pygame.error as exc:
            print(f"[engine] No pude cargar icono '{icon_path}': {exc}")
        self.clock = pygame.time.Clock()
        self.menu_scene = MenuScene(self.screen, self.clock)
        self.match_scene = MatchScene(self.screen, self.clock)
        sfx.load_sounds()

    def run(self):
        self.initialise()
        state = "menu"

        while self.running:
            if state == "menu":
                selection = self.menu_scene.run()
                if selection == "solo":
                    state = "match_solo"
                elif selection == "versus":
                    state = "match_versus"
                else:
                    state = "quit"
            elif state == "match_solo":
                sfx.play_ambiente()
                result = self.match_scene.run(p2_is_ai=True)
                sfx.stop_ambiente()
                state = "menu" if result == "menu" else "quit"
            elif state == "match_versus":
                sfx.play_ambiente()
                result = self.match_scene.run(p2_is_ai=False)
                sfx.stop_ambiente()
                state = "menu" if result == "menu" else "quit"
            elif state == "quit":
                self.running = False

        pygame.quit()
        sys.exit()

