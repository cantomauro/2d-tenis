# world_to_iso(x,y, ox=0, oy=0), orden de pintado (clave por iso_y/x+y), helpers de offset.

def world_to_iso(x, y, ox=0, oy=0):
    return (x - y) + ox, (x + y) / 2 + oy

def depth_key_from_world(x, y):
    # Orden por iso_y ~ (x+y)/2
    return (x + y)
