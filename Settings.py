# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,191,250)
YELLOW = (255,255,0)
# -- Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 60
# -- Game Options
WIDTH = 1080
LENGTH = 500
FPS = 60
gameplay_side= True
FONT_NAME = "arial"
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"
SPRITESHEET_PLAYER = "p1_spritesheet.png"
# -- Starting platforms
PLATFORM_LIST = [(0, LENGTH - 50),
                 (WIDTH / 2 - 50, LENGTH * 3 / 4),
                 (150, LENGTH - 250),
                 (180, 200),
                 (500, -50)]
