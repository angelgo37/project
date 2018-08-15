# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
# -- Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
# -- Game Options
WIDTH = 640
LENGTH = 480
FPS = 60
gameplay_side= True
# -- Starting platforms
PLATFORM_LIST = [(0, LENGTH - 40, 9999, 40),
                 (WIDTH / 2 - 50, LENGTH * 3 / 4, 100, 20),
                 (150, LENGTH - 250, 100, 20),
                 (180, 100, 200, 20),
                 (0, -2000, 20, 2000 + LENGTH)]
##                 (WIDTH - 20, -2000, 20, 3000),
##                 (500, -50, 200, 20)]
