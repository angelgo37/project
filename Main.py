import pygame as pg
import random
from Settings import *
from sprite2 import *
from os import path 

class Game:
    def __init__(self):
        # -- Initialise PyGame
        pg.init()
        pg.mixer.init
        # -- Blank Screen
        size = (WIDTH,LENGTH)
        self.screen = pg.display.set_mode(size)
        # -- Title of new window/screen
        pg.display.set_caption("My Window")
        # -- Game running flag set to true
        self.running = True
        # -- Manages how fast screen refreshes
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # -- Loads High score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir,"img")
        with open(path.join(self.dir, HS_FILE), "r+") as f: 
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # -- Load image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.spritesheet_player = Spritesheet(path.join(img_dir, SPRITESHEET_PLAYER))
        # -- Load Sounds
        self.snd_dir = path.join(self.dir,"snd")
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, "Jump.wav"))

    def new(self):
        # -- New Game
        self.all_sprites = pg.sprite.Group()
        self.score = 0
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        # -- Platforms
        for plat in PLATFORM_LIST:
            # -- Explode the list into its 4 components
            p = Platform(self,*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        pg.mixer.music.load(path.join(self.snd_dir, "Happy.mp3"))
        # -- Running the Game
        self.run()
        

    def run(self):
        # -- Game Loop
        pg.mixer.music.play(loops = -1)
        self.playing = True
        while self.playing:
            # - The clock ticks over
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)
        
    def update(self):
        # -- Game Loop Update
        self.all_sprites.update()
        # -- Only land when falling
        if self.player.vel.y > 0:
            # -- Check for collisions to land
            coll = pg.sprite.spritecollide(self.player, self.platforms, False)
            if coll:
                lowest = coll[0]
                for collision in coll:
                    if collision.rect.bottom > lowest.rect.bottom:
                        lowest = collision
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False
        # -- Screen scrolls
        if self.player.rect.top <= LENGTH/4:
            self.player.pos.y += max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y),2)
                if plat.rect.top >= LENGTH:
                    plat.kill()
                    self.score += 10

        # -- Game Over
        if self.player.rect.bottom > LENGTH:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y,10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
##        # -- Screen scrolls
##        if self.player.rect.right >= 2*WIDTH / 3:
##            self.player.pos.x -= max(abs(self.player.vel.x),2)
##            for plat in self.platforms:
##                plat.rect.x -= max(abs(self.player.vel.x),2)
##                if plat.rect.right <= 0:
##                    plat.kill()
##        if self.player.rect.left <= 180:
##            self.player.pos.x += max(abs(self.player.vel.x),2)
##            for plat in self.platforms:
##                plat.rect.x += max(abs(self.player.vel.x),2)
##                if plat.rect.left >= WIDTH:
##                    plat.kill()
##
##        while len(self.platforms) <10:
##            width = random.randrange (50,100)
##            p = Platform(random.randrange(WIDTH,WIDTH*2),
##                         random.randrange(0, LENGTH),
##                         width, 20)
##            self.platforms.add(p)
##            self.all_sprites.add(p)
        while len(self.platforms) <20:
            width = random.randrange (50,100)
            p = Platform(self, random.randrange(0,WIDTH - width),
                         random.randrange(-LENGTH, -30))
            self.platforms.add(p)
            self.all_sprites.add(p)
            
        
    def events(self):
        # -- Game Loop - draw
        # -- User input and controls
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
            

    def draw(self):
        # -- Draw Loop
        self.screen.fill (BLUE)
        self.all_sprites.draw(self.screen)
        self.game_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        self.screen.blit(self.player.image, self.player.rect)
        # -- Flip the display   
        pg.display.flip()

    def show_start_screen(self):
        # -- Start screen
        pg.mixer.music.load(path.join(self.snd_dir, "menu.mp3"))
        pg.mixer.music.play(loops = -1)
        self.screen.fill(BLUE)
        self.game_text("My Game", 48, WHITE, WIDTH / 2, LENGTH / 4)
        self.game_text("Move with the arrows and press Space to jump", 22, WHITE, WIDTH / 2, LENGTH * 3/4)
        self.game_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.start_wait()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # -- Game over screen
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, "gameover.ogg"))
        pg.mixer.music.play(loops = -1)
        self.screen.fill(BLUE)
        self.game_text("GAME OVER", 48, WHITE, WIDTH / 2, LENGTH / 4)
        self.game_text("Press a key to play again", 22, WHITE, WIDTH / 2, LENGTH / 2)
        self.game_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, LENGTH * 3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.game_text("New High Score", 22, WHITE, WIDTH / 2, LENGTH / 2 + 40)
            with open(path.join(self.dir, HS_FILE), "r+") as f:
                f. write(str(self.score))
        else:
            self.game_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.start_wait()
        pg.mixer.music.fadeout(500)

    def start_wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
                    

    def game_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        
    

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
