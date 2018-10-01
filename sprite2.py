import pygame as pg
from Settings import *
vec = pg.math.Vector2
import random

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        
    def get_image(self,x,y,width,height):
        # -- Gets image from sprite sheet
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width, height))
        return image

    def get_image_platform(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width, height))
        image = pg.transform.scale(image, (width // 3, height // 3))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.moving = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (40, LENGTH -100)
        self.pos = vec(40, LENGTH-100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def load_images(self):
        self.standing_frames_r = [self.game.spritesheet_player.get_image(67 ,196 ,66, 92)]
        self.standing_frames_l = []
        for frame in self.standing_frames_r:
            frame.set_colorkey(BLACK)
            self.standing_frames_l.append(pg.transform.flip(frame, True, False))
        self.moving_frames_r = [self.game.spritesheet_player.get_image(0 ,0 ,72, 97),
                                self.game.spritesheet_player.get_image(73 ,0 ,72, 97),
                                self.game.spritesheet_player.get_image(146, 0, 72, 97),
                                self.game.spritesheet_player.get_image(0, 98, 72, 97),
                                self.game.spritesheet_player.get_image(73, 98, 72, 97),
                                self.game.spritesheet_player.get_image(146, 98, 72, 97),
                                self.game.spritesheet_player.get_image(219, 0, 72, 97),
                                self.game.spritesheet_player.get_image(292, 0, 72, 97),
                                self.game.spritesheet_player.get_image(219, 98, 72, 97),
                                self.game.spritesheet_player.get_image(365, 0, 72, 97),
                                self.game.spritesheet_player.get_image(292, 98, 72, 97)]
        self.jump_frames_r = [self.game.spritesheet_player.get_image(438, 93, 67, 94)]
        self.moving_frames_l = []
        self.jump_frames_l = []
        for frame in self.moving_frames_r:
            frame.set_colorkey(BLACK)
            self.moving_frames_l.append(pg.transform.flip(frame, True, False))
        for frame in self.jump_frames_r:
            frame.set_colorkey(BLACK)
            self.jump_frames_l.append(pg.transform.flip(frame, True, False))
            
    def jump(self):
        # -- Player can only jump when standing on platform
        self.rect.x +=2
        coll = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if coll and not self.jumping:
            self.game.jump_sound.play()
            self.image = self.game.spritesheet_player.get_image(438, 93, 67, 94)
            self.jumping = True
            # -- Creating jump physics
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        # -- Smaller Jump
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
        

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # Wrap the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x > 0.05 or self.vel.x < -0.05:
            self.moving = True
        else:
            self.moving = False
        if self.moving and not self.jumping:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame +1) % len(self.moving_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.moving_frames_r[self.current_frame]
                else:
                    self.image = self.moving_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if not self.jumping and not self.moving:
            if now - self.last_update > 320:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames_r)
                bottom = self.rect.bottom
                if self.vel.x !=0:
                    if self.vel.x > 0:
                        self.image = self.standing_frames_r[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                    if self.vel.x < 0:
                        selfimage = self.standing_frames_l[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                else:
                    self.image = self.standing_frames_r[self.current_frame]
        if self.jumping and self.moving:
            if now - self.last_update >10:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0.01 or self.vel.x < -0.01:
                    if self.vel.x > 0.01:
                        self.image = self.jump_frames_r[self.current_frame]
                    else:
                        self.image = self.jump_frames_l[self.current_frame]
            

class Platform (pg.sprite.Sprite):
    def __init__(self,game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images =[self.game.spritesheet.get_image_platform(0,288,380,94),
                 self.game.spritesheet.get_image_platform(213,1662,201,100)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
