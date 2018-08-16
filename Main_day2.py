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
        # -- Manages how fast screen refreshes
        self.clock = pg.time.Clock()

    def new(self):
        # -- New Game
        self.all_sprites = pg.sprite.Group()
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
        # -- Flip the display
        pg.display.flip()

    def show_start_screen(self):
        # -- Start screen
        pass

    def show_go_screen(self):
        # -- Game over screen
        pass
    

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
