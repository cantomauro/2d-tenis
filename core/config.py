# Constantes globales centralizadas (resolución, colores, velocidades, tamaños, bindings).

# --- Presentación / ventana ---
SCREEN_W, SCREEN_H = 1024, 768
SCREEN_SIZE = (SCREEN_W, SCREEN_H)
FPS = 60
BG_COLOR = (18, 18, 22)
WINDOW_ICON_SCALE = 1
CROWD_BG_SCALE = .7  # 1.0 = pantalla completa; <1 reduce el fondo, >1 lo agranda
CROWD_BG_OFFSET = (-150, -100)  # Ajusta la posición final del PNG (x, y)
CROWD_SIDE_SCALE = .7      # Escala de la tribuna lateral (detrás del jugador 2)
CROWD_SIDE_OFFSET = (20, -60)   # Offset relativo al ancla (top-right) de la tribuna lateral
CROWD_LEFT_SCALE = 0.85    # Escala de la segunda tribuna (lado izquierdo)

# --- Opciones visuales ---

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
