import pygame as pg
import random
from Settings import *
from Sprite import *

class Game:
    def __init__(self):
        # -- Initialise PyGame
        pg.init()
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
        self.player = Player()
        self.all_sprites.add(self.player)
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
        coll = pg.sprite.spritecollide(self.player, self.platforms, False)
        if coll:
            self.player.pos.y = coll[0].rect.top + 1
            self.player.vel.y = 0
        
    def events(self):
        # -- Game Loop - draw
        # -- User input and controls
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False

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
