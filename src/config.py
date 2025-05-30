WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
GRID_ROWS = 13
GRID_COLS = 6

BASE_FALL_SPEED = 10000

BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (200, 200, 200)
JEWEL_COLORS = {
    'S': (255,   0,   0),
    'T': (  0, 255,   0),
    'V': (  0,   0, 255),
    'W': (255, 255,   0),
    'X': (255, 165,   0),
    'Y': (128,   0, 128),
    'Z': (  0, 255, 255),
    ' ': BACKGROUND_COLOR,
}

# Music files
MENU_MUSIC = "./assets/menu.ogg"
GAME_MUSIC = "./assets/game.ogg"

# Application states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2
STATE_SAVE = 3
STATE_LEADERBOARD = 4