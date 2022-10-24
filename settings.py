import pygame

WINDOW_SIZE = (1920, 1080)

ENABLE_EMULATOR = True

# LED Strip settings
FRAMERATE = 60
PIXEL_COUNT = 580
SEG_WIDTH = 12

# Segment numbers
BOXES = ((2, 22, 4, 23),
         (3, 24, 5, 25),
         (6, 26, 8, 27),
         (7, 28, 9, 29),
         (10, 30, 12, 31),
         (11, 32, 13, 33),
         (14, 34, 16, 35),
         (15, 36, 17, 37),
         (18, 38, 20, 39),
         (19, 40, 21, 41))
RAILS = (0, 1)
GRID = tuple(i for i in range(2, 42))
ALL_SEGS = tuple(i for i in range(42))

# Keys
KEY_START = pygame.K_f
BOX_KEYS = [pygame.K_v, pygame.K_y,
             pygame.K_d, pygame.K_j,
             pygame.K_a, pygame.K_z,
             pygame.K_m, pygame.K_w,
             pygame.K_x, pygame.K_t]
KEY_RELAY_ENABLE = pygame.K_r
KEY_RELAY_DISABLE = pygame.K_t

# Tutorial box numbers
TUTORIAL_BOXES = (5, 0, 8)

# Size of rectangles to blit during game phase
RECT_START_X = 200
RECT_START_Y = 200
RECT_SIZE = 200
RECT_SPACING = 50

# Game settings
WHACK_TIME = 10  # How many seconds before a tile despawns
WIN_PERCENT = 0.7  # The percentage of tiles that must be whacked to win
