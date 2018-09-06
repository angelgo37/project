import pygame as pg
import random
from Settings import *
from sprite2 import *

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
        self.high_score = 0
        # -- Manages how fast screen refreshes
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)

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
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        # -- Running the Game
        self.run()
        

    def run(self):
        # -- Game Loop
        self.playing = True
        while self.playing:
            # - The clock ticks over
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
    def update(self):
        # -- Game Loop Update
        self.all_sprites.update()
        # -- Only land when falling
        if self.player.vel.y > 0:
            # -- Check for collisions to land
            coll = pg.sprite.spritecollide(self.player, self.platforms, False)
            if coll:
                self.player.pos.y = coll[0].rect.top + 1
                self.player.vel.y = 0
        # -- Screen scrolls
        if self.player.rect.top <= LENGTH/4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
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
        while len(self.platforms) <10:
            width = random.randrange (50,100)
            p = Platform(random.randrange(0,WIDTH - width),
                         random.randrange(-LENGTH, -30),
                         width, 20)
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
            

    def draw(self):
        # -- Draw Loop
        self.screen.fill (BLACK)
        self.all_sprites.draw(self.screen)
        self.game_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # -- Flip the display
        pg.display.flip()

    def show_start_screen(self):
        # -- Start screen
        self.screen.fill(BLACK)
        self.game_text("My Game", 48, WHITE, WIDTH / 2, LENGTH / 4)
        self.game_text("Move with the arrows and press Space to jump", 22, WHITE, WIDTH / 2, LENGTH * 3/4)
        pg.display.flip()
        self.start_wait()

    def show_go_screen(self):
        # -- Game over screen
        if not self.running:
            return
        if self.score > self.high_score:
            print("poop")
            self.high_score = self.score
        self.screen.fill(BLACK)
        self.game_text("GAME OVER", 48, WHITE, WIDTH / 2, LENGTH / 4)
        self.game_text("Press a key to play again", 22, WHITE, WIDTH / 2, LENGTH / 2)
        self.game_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, LENGTH * 3/4)
        self.game_text("High score: " + str(self.high_score), 22, WHITE, WIDTH / 2 , (LENGTH * 1/3) + 150)
        pg.display.flip()
        self.start_wait()

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
