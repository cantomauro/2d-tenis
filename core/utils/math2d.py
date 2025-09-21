# helpers geométricos (clamp, normalización, distancia, reflejos).

def clamp(v, lo, hi): return max(lo, min(hi, v))

def length2(dx, dy): return (dx*dx + dy*dy) ** 0.5

def normalize(dx, dy, eps=1e-6):
    L = max(eps, length2(dx, dy))
    return dx / L, dy / L

def reflect(vx, vy, nx, ny):
    # v' = v - 2*(v·n)*n ; n normalizada
    dot = vx*nx + vy*ny
    return vx - 2*dot*nx, vy - 2*dot*ny
