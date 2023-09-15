import pygame as pg
import pygame.key
from config import *
import sys
import math
import random
import serial

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.player
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.joy = 'neu'
        self.facing = 'down'

        image_load = pg.image.load("img/rover.png")


        self.x_change = 0
        self.y_change = 0

        self.image = pg.Surface([self.width,self.height])
        self.image.blit(image_load, (0,0))
        self.image.set_colorkey(white)
        self.font = pygame.font.Font('Roboto-Regular.ttf', 32)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.welcome_timer = 0


        self.display_welcome = False

    def update(self):
        self.move()
        self.animate()
        self.collide_thing()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0


    def move(self):
        keys = pygame.key.get_pressed()
        hits = pg.sprite.spritecollide(self, self.game.obs, False)
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                if not hits:
                    sprite.rect.x += player_speed
            self.x_change-= player_speed
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                if not hits:
                    sprite.rect.x -= player_speed
            self.x_change+= player_speed
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                if not hits:
                    sprite.rect.y += player_speed
            self.y_change-= player_speed
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                if not hits:
                    sprite.rect.y -= player_speed
            self.y_change+= player_speed
            self.facing = 'down'




    def collide_blocks(self, direction):
        if direction == "x":
            # Check for collisions in the x direction
            hits = pg.sprite.spritecollide(self, self.game.obs, False)
            if hits:
                if self.x_change > 0:
                    # Adjust the sprite's position when moving right
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x+= player_speed
                elif self.x_change < 0:
                    # Adjust the sprite's position when moving left
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x-= player_speed
        elif direction == "y":
            # Check for collisions in the y direction
            hits = pg.sprite.spritecollide(self, self.game.obs, False)
            if hits:
                if self.y_change > 0:
                    # Adjust the sprite's position when moving down
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y+= player_speed
                elif self.y_change < 0:
                    # Adjust the sprite's position when moving up
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y-= player_speed


    def collide_thing(self):
        hits = pg.sprite.spritecollide(self, self.game.thing, False)
        if hits:
            self.kill()
            self.game.playing = False

    def animate(self):
        if self.facing == 'down':
            self.image = pg.image.load("img/rover_down.png")
            self.image.set_colorkey(white)
        elif self.facing == 'up':
            self.image = pg.image.load("img/rover_up.png")
            self.image.set_colorkey(white)
        elif self.facing == 'left':
            self.image = pg.image.load("img/rover_left.png")
            self.image.set_colorkey(white)
        elif self.facing == 'right':
            self.image = pg.image.load("img/rover.png")
            self.image.set_colorkey(white)



class thing(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = THING_LAYER
        self.groups = self.game.all_sprites, self.game.thing
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        image_load = pg.image.load("img/thing.png")

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.movement_loop = 0
        self.travel = random.randint(7, 13)

        self.image = pg.Surface([self.width, self.height])
        self.image.blit(image_load, (0, 0))
        self.image.set_colorkey(white)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self):
        if self.facing == 'left':
            self.x_change-= thing_speed
            self.movement_loop-=1
            if self.movement_loop<= -self.travel:
                self.facing='right'
        if self.facing == 'right':
            self.x_change+= thing_speed
            self.movement_loop+=1
            if self.movement_loop>= self.travel:
                self.facing='left'
        if self.facing == 'up':
            self.y_change+= thing_speed
            self.movement_loop+=1
            if self.movement_loop>= self.travel:
                self.facing='down'
        if self.facing == 'down':
            self.y_change-= thing_speed
            self.movement_loop-=1
            if self.movement_loop<= -self.travel:
                self.facing='up'



    def update(self):
        self.move()

        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = 0
        self.y_change = 0




class block(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.obs
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size
        image_load = pg.image.load("img/rock.png")
        self.image = pg.Surface([self.width, self.height])
        self.image.blit(image_load, (0, 0))
        self.image.set_colorkey(white)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class ground(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        image_load = pg.image.load("img/ground.png")
        self.image = pg.Surface([self.width, self.height])
        self.image.blit(image_load, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class button:
    def __init__(self, x, y,width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('PressStart2P-Regular.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))

        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Quest(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.q
        pg.sprite.Sprite.__init__(self, self.groups)
        self.q = q

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size
        images = random.choice(['img/q1.png', 'img/q2.png', 'img/q3.png'])
        image_load = pg.image.load(images)
        self.image = pg.Surface([self.width, self.height])
        self.image.blit(image_load, (0, 0))
        self.image.set_colorkey(white)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.collide()

    def collide(self):
        hits = pg.sprite.spritecollide(self, self.game.player, False)
        if hits:
            self.kill()
            self.game.q_count += 1
            self.game.los_i += 1


