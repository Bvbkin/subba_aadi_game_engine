# This file was created by: Aadi Subba

# import libraries
import pygame as pg
from settings import *
from sprites import *
import sys
from random import randint
from os import path

from math import floor

'''

Game design truths:
goals, rules, feedback, freedom, whats the verb, and will it form a sentence

Health Bar
Following enemy
Weapons and projectiles

'''
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 32
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Cooldown():
    # set all properties to zero when instantiated
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensure the timer is counting
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.data
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

# creating a class named Game
class Game:
    # define a method with parameter 'self'
    def __init__(self):
        pg.init()
        # set width and height for display
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # set caption for display
        pg.display.set_caption("My first video game!")
        # set time clock for display
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.running = True
        # stores game info with this, ex. high scores
        self.load_data()
        self.playing = True
    
    # importing map data from the file map.txt
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'monkey.png')).convert_alpha()
        self.mob1_img = pg.image.load(path.join(img_folder, 'mob1.png')).convert_alpha()
        self.map_data = []
 
        '''
        with is a context manager, helps close or release resources
        after they are used, it prevents errors.
    
        '''
        # open map.txt and add lines into list (line)
        with open (path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    # add player sprite to Group
    def new(self):
        self.test_timer = Cooldown()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.speedpotion = pg.sprite.Group()
        self.healthpotion = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        self.player = pg.sprite.Group()
        # self.player = Player(self,10,10)
        # self.all_sprites.add(self.player)
        
        #for x in range(10,20):
            #Wall(self,x,5)
        
        # might print walls
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == 'x':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'm':
                    Mob(self,col,row)
                if tile == 'C':
                    Coin(self,col,row)
                if tile == 's':
                    speedpotion(self,col,row)
                if tile == 'h':
                    healthpotion(self,col,row)

    # runs the game, game won't run without it
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # input
            self.events()
            # processing
            self.update()
            # output
            self.draw()
    
    # quits the game when you click the red x
    def quit(self):
        pg.quit()
        sys.exit()

    # method; tied to the class
    def input(self):
        pass

    # updates the position of all sprites on the grid
    def update(self):
        self.all_sprites.update()
        if self.player.health <= 0:
            self.playing = False
        

    # draws the grid for our game
    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        
        for y in range (0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH,y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    # paints the background black & draws grid lines
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 32, WHITE, 1, 1)
        self.draw_text(self.screen, str(self.player.health), 32, WHITE, 30, 1)
        draw_health_bar(self.screen, self.player.rect.x, self.player.rect.y-8, self.player.health)

        pg.display.flip()

    def events(self):
        # listening for events
        for event in pg.event.get():
            # when you hit the red x the window closes and ends
            if event.type == pg.QUIT:
                self.quit()
                print ("the game has ended...")
            # player movement via arrow keys
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=+1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=+1)
            
    
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play!", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.playing:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "You died - press any key to play again!", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# call the class to run it
g = Game()
g.show_start_screen()

while True:
    g.new()
    g.run()
    g.show_go_screen()
