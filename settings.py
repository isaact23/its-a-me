import pygame
from colors import *

# GUI Settings
WINDOW_SIZE = (800, 560)
ENABLE_EMULATOR = True

STAR_FRAMERATE = 32
STAR_FRAMES = 32
BOWSER_FRAMERATE = 30
BOWSER_FRAMES = 62
CLOUD_FRAMERATE = 5
CLOUD_ANIMATION_SECS = 12
CLOUD_FRAMES = 59
GOOMBA_FRAMERATE = 4
GOOMBA_ANIMATION_SECS = 5
GOOMBA_FRAMES = 2
MARIO_FRAMERATE = 5
MARIO_ANIMATION_SECS = 7
MARIO_FRAMES = 11
TOAD_TEXT_FRAMERATE = 12

TOAD_TEXT1 = "Hi! I need your help to collect"
TOAD_TEXT2 = "the power stars! Step on the"
TOAD_TEXT3 = "square to start!"
TOAD_TEXT4 = "Great! Keep it up!"
TOAD_TEXT5 = "One square to go!"
TOAD_TEXT6 = "Great! Get ready!"
TOAD_TEXT7 = "Hooray! You win!"

# LED Strip settings
FRAMERATE = 60
PIXEL_COUNT = 580
SEG_WIDTH = 12

# Keys
BOX_KEYS = [pygame.K_v, pygame.K_y,
             pygame.K_d, pygame.K_j,
             pygame.K_a, pygame.K_z,
             pygame.K_m, pygame.K_w,
             pygame.K_x, pygame.K_t]
KEY_MUSHROOM_DOWN = pygame.K_r
KEY_MUSHROOM_UP = pygame.K_e

# Tutorial box numbers
TUTORIAL_BOXES = (5, 0, 8)

# Size of rectangles to blit during game phase
RECT_START_X = 100
RECT_START_Y = 200
RECT_SIZE = 100
RECT_SPACING = 25

# Game settings
WHACK_TIME = 10  # How many seconds before a tile despawns
WIN_PERCENT = 0.7  # The percentage of tiles that must be whacked to win

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
