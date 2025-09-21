# clase base Entity con world_pos, update(dt), draw(surface), y depth_key (para orden por iso_y).

from core.iso.projection import world_to_iso, depth_key_from_world

class Entity:
    def __init__(self, x, y):
        self.x, self.y = x, y  # mundo

    def update(self, dt): pass

    def screen_pos(self, ox=0, oy=0):
        return world_to_iso(self.x, self.y, ox, oy)

    def depth_key(self):
        return depth_key_from_world(self.x, self.y)

    def draw(self, surface, ox=0, oy=0):
        pass
