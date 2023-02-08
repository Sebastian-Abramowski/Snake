from pygame import font, USEREVENT

FPS = 60

# Colours
BLACK = (0, 0, 0)
BLACK1 = (26, 26, 26)
BLACK3 = (35, 35, 35)
BLACK2 = (45, 45, 45)
WHITE = (255, 255, 255)
RED = (100, 0, 50)
GREEN = (31, 97, 52)

# Window
MIN_WIDTH = 780
MIN_HEIGHT = 500
PADDING = 50
SQUARE_SIZE = 100

# Font
font.init()
FONT = font.SysFont('calibri', 20, True)

# Game
SOUND_EFFECTS = 1
ICON_SIZE = (40, 40)
DELAY_BETWEEN_MOVES = 350

# Events
EXTRA_SPEED_EVENT = USEREVENT + 2
NORMAL_SPEED_EVENT = USEREVENT + 3
END_OF_THE_GAME_EVENT = USEREVENT + 5
MOVING_SNAKE_EVERY_SEC_EVENT = USEREVENT + 1
SNAKE_COLLISION = USEREVENT + 4
COLLISION_WITH_WALL_EVENT = USEREVENT
