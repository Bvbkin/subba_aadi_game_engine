# This file was created by: Aadi Subba
# Appreciation to Chris Bradfield
import pygame as pg
from sys import *
from settings import *
from random import randint
from os import path
from pygame.sprite import Sprite


dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')

# creates vectors for movement
vec = pg.math.Vector2

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width, height))
        return image

# write a player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE,TILESIZE))
        # self.image = game.player_img
        # self.image.fill(GREEN)
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]
        self.current_frame = 0
        self.last_update = 0
        self.material = True
        self.jumping = False
        self.walking = False
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.health = 100
        self.sword_drawn = False
        self.sword_dir = (0,0)
        self.sword = Sword(self.game, self.rect.x, self.rect.y, 16, 16, (0,0))

    # sets direction
    def set_dir(self, d):
        self.dir = d
        # return (0,0)
    # gets direction
    def get_dir(self):
        return self.dir
    # gets mouse input
    def get_mouse(self):
        if pg.mouse.get_pressed()[0]:
            # mx = pg.mouse.get_pos()[0]
            # my = pg.mouse.get_pos()[1]
            if self.weapon_drawn == False:
                self.weapon_drawn = True
                if abs(pg.mouse.get_pos()[0]-self.rect.x) > abs(pg.mouse.get_pos()[1]-self.rect.y):
                    if pg.mouse.get_pos()[0]-self.rect.x > 0:
                        print("swing to pos x")
                        self.weapon = Sword(self.game, self.rect.x+TILESIZE, self.rect.y, 32, 5, (1,0))
                    if pg.mouse.get_pos()[0]-self.rect.x < 0:
                        print("swing to neg x")
                        self.weapon = Sword(self.game, self.rect.x-TILESIZE, self.rect.y, 32, 5, (-1,0))
                else:
                    if pg.mouse.get_pos()[1]-self.rect.y > 0:
                        print("swing to pos y")
                        self.weapon = Sword(self.game, self.rect.x, self.rect.y+self.rect.height, 5, 32, (0,1))
                    if pg.mouse.get_pos()[1]-self.rect.y < 0:
                        print("swing to neg y")
                        self.weapon = Sword(self.game, self.rect.x, self.rect.y-self.rect.height, 5, 32, (0,-1))

        if pg.mouse.get_pressed()[1]:
            print("middle click")
        if pg.mouse.get_pressed()[2]:
            print("right click")


    # movement with WASD
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_s]:
            self.vy = self.speed

    # collision for player & walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    # collisions with other classes
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "speedpotion":
                self.speed += 75
            if str(hits[0].__class__.__name__) == "healthpotion":
                if self.health <= 80:
                    self.health += 20
                elif self.health == 100:
                    self.collide_with_group("healthpotion", False)
                else:
                    self.health += 100-self.health
            if str(hits[0].__class__.__name__) == "Mob":
                self.health -= 4
            if str(hits[0].__class__.__name__) == "poisoncloud":
                self.health -= 5

    # collision for player & enemy
    def collide_with_mobs(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.mobs, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.mobs, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32),

                                ]
        self.walking_frames = [
                                self.spritesheet.get_image(64,0, 32, 32),
                                self.spritesheet.get_image(96,0, 32, 32),
                                ]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            if not self.walking:
                self.image = self.standing_frames[self.current_frame]
            else:
                self.image = self.walking_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    # old motion

    # player movement 
    # def move(self, dx=0,dy=0):
    #     self.x += dx
    #     self.y += dy
    

    # new motion

    # UPDATE THE UPDATE
    # runs all function inside player class
    def update(self):
        # self.rect.x = self.x
        # self.rect.y = self.y
        self.animate()
        self.get_keys()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.speedpotion, True)
        self.collide_with_group(self.game.healthpotion, True)
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.poisoncloud, False)
        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")

# write a wall class
class Wall(pg.sprite.Sprite):
    def __init__(self, game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0
    
    # updates the walls
    def update(self):
        # self.rect.x += 1
        self.rect.x += TILESIZE * self.speed
        # self.rect.y += TILESIZE * self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
        # if self.rect.y > HEIGHT or self.rect.y < 0:
            # self.speed *= -1

# creating an enemy class
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.image = self.game.mob1_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = (4,7)
        self.health = 5
        print("created mob at", self.rect.x, self.rect.y)
    
    # creates mob + wall collision
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    # using player location to chase player
    def chasing(self):
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
    
    # updates functions inside mob class
    def update(self):
        if self.health < 1:
            self.kill()
        # self.image.blit(self.game.screen, self.pic)
        # pass
        # self.rect.x += 1
        self.chasing()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

'''
class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.mob_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(ORANGE)
        self.image = self.game.mob1_img
        # self.image.set_colorkey(BGCOLOR)
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 500
        # added
        self.speed = 100
        self.chasing = True
        # self.health = MOB_HEALTH
        self.health = 5
    def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    
    def update(self):
        if self.health <= 0:
            self.kill()
        # self.sensor()
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob1_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            # equation of motion
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # hit_rect used to account for adjusting the square collision when image rotates
            self.hit_rect.centerx = self.pos.x
            self.collide_with_walls('x')
            self.hit_rect.centery = self.pos.y
            self.collide_with_walls('y')
            self.rect.center = self.hit_rect.center
'''
            
# create a coin class
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.banana_img
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# create a speedpotion class
class speedpotion(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.speedpotion
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.speedpotion_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# create a healthpotion class
class healthpotion(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.healthpotion
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.medkit_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# creates a class for sword
class Sword(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, dir):
        self.groups = game.all_sprites, game.sword
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.rect.width = w
        self.rect.height = h
        self.pos = vec(x,y)
        self.dir = dir
        print("I created a sword")
    
    # sword and mob collision
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                print("you hurt a mob!")
                hits[0].health -= 1
            # if str(hits[0].__class__.__name__) == "Mob2":
                # print("you hurt a mob!")
                # hits[0].health -= 1
    
    # tracks the movement/location of sword
    def track(self, obj):
        self.vx = obj.vx
        self.vy = obj.vy
        self.rect.width = obj.rect.x+self.dir[0]*32+5
        self.rect.width = obj.rect.y*self.dir[1]*32+5
    
    # updates the functions and sword
    def update(self):
        if self.game.player.sword_drawn == False:
            self.kill()
        self.track(self.game.player)
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_group(self.game.mobs, False)

'''
class Shield(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, dir):
        self.groups = game.all_sprites, game.shield
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.rect.width = w
        self.rect.height = h
        self.pos = vec(x,y)
        self.dir = dir
        print("I created a shield")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                print("you hurt a mob!")
                hits[0].health -= 1
            if str(hits[0].__class__.__name__) == "Mob2":
                print("you hurt a mob!")
                hits[0].health -= 1
    def track(self, obj):
        self.vx = obj.vx
        self.vy = obj.vy
        self.rect.width = obj.rect.x+self.dir[0]*32+5
        self.rect.width = obj.rect.y*self.dir[1]*32+5
    def update(self):
        if self.game.player.shield_drawn == False:
            self.kill()
        self.track(self.game.player)
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_group(self.game.mobs, False)
'''
'''
class poisoncloud(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.poisoncloud
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.image = self.game.poison_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        print("created cloud at", self.rect.x, self.rect.y)
    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx += 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy += 0
                self.rect.y = self.y\
    
    def update(self):
        # self.image.blit(self.game.screen, self.pic)
        # pass
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
'''

# class for poison cloud
class poisoncloud(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.poisoncloud
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image = game.poison_img
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 300

    # movement with WASD
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT]:
            self.vx = self.speed
        if keys[pg.K_UP]:
            self.vy = -self.speed
        if keys[pg.K_DOWN]:
            self.vy = self.speed

    # collision for storm & walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # UPDATE THE UPDATE
    # calls the functions inside poison cloud and updates it
    def update(self):
        # self.rect.x = self.x
        # self.rect.y = self.y
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE

class Teleport(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.teleport
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image = game.teleport_img
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    # collision for teleport & walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # UPDATE THE UPDATE
    def update(self):
        # self.rect.x = self.x
        # self.rect.y = self.y
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
