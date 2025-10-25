# Constantes globales centralizadas (resolución, colores, velocidades, tamaños, bindings).

# --- Presentación / ventana ---
SCREEN_W, SCREEN_H = 1024, 768
SCREEN_SIZE = (SCREEN_W, SCREEN_H)
FPS = 60
BG_COLOR = (18, 18, 22)

# --- HUD / mensajes ---
P1_MSG_COLOR = (64, 160, 255)
P2_MSG_COLOR = (220, 70, 70)

# --- Juego / cancha ---
SERVE_DELAY = 1.0  # segundos
TARGET_SCORE = 7

COURT_X, COURT_Y = 0, 0
COURT_W, COURT_H = 380, 600

# --- Física de la pelota ---
BALL_HIT_SPEED = 320       # px/s
BALL_HIT_COOLDOWN = 0.18   # segundos (~11 frames a 60 FPS)
MAX_HIT_ANGLE_X = 0.75     # 0..1 (0=recto, 1≈45°)
