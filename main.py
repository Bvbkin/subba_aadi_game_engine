# This file was created by: Aadi Subba

# import libraries
import pygame as pg
from settings import *
from sprites import *
import sys
from random import randint
from os import path
from tilemap import *
from weather import *
from math import floor
from utils import *

'''

Game design truths:
goals, rules, feedback, freedom, whats the verb, and will it form a sentence

Health Bar
Following enemy
Obstacle

BETA Goals:
*Improve mob intelligence

Gameplay goal: Level progression

Secondary goal: add weapons and enemy health

'''

map1 = "map1.txt"
map2 = "map2.txt"
map3 = "map3.txt"
map4 = "map4.txt"

maps = [map1, map2, map3, map4]

# create the health bar above player
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 32
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    # set colors for health bar
    if pct >= 80:
        pg.draw.rect(surf, GREEN, fill_rect)
    elif pct < 80 and pct >= 30:
        pg.draw.rect(surf, YELLOW, fill_rect)
    elif pct < 30:
        pg.draw.rect(surf, RED, fill_rect)
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
        self.playing = True
        self.paused = False
        self.current_map = 0
        self.load_data()
    
    # importing map data from the file map.txt
    # import images to sprites
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        # self.player_img = pg.image.load(path.join(img_folder, 'monkey.png')).convert_alpha()
        self.map = Map(path.join(game_folder, maps[self.current_map]))
        self.mob1_img = pg.image.load(path.join(img_folder, 'mob1.png')).convert_alpha()
        self.banana_img = pg.image.load(path.join(img_folder, 'banana.png')).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, 'wall.jpg')).convert_alpha()
        self.medkit_img = pg.image.load(path.join(img_folder, 'medkit.png')).convert_alpha()
        self.speedpotion_img = pg.image.load(path.join(img_folder, 'speedpotion.png')).convert_alpha()
        # self.poison_img = pg.image.load(path.join(img_folder, 'poisoncloud.png')).convert_alpha()
        self.teleport_img = pg.image.load(path.join(img_folder, 'teleport.png')).convert_alpha()
        self.background_img = pg.image.load(path.join(img_folder, 'background.png')).convert_alpha()
        self.background_rect = self.background_img.get_rect()
        # self.map_data = []
 
        '''
        with is a context manager, helps close or release resources
        after they are used, it prevents errors.
    
        '''
        # open map.txt and add lines into list (line)
        # with open (path.join(game_folder, 'map1.txt'), 'rt') as f:
            # for line in f:
                # print(line)
                # self.map_data.append(line)
    def change_map(self, lvl):
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # reset criteria for changing level
        self.player.moneybag = 0
        # reset map data list to empty
        self.map_data = []
        # reset weather
        self.surface = self.randomweather.generate_weather()
        # open next level
        with open(path.join(game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        # repopulate the level with stuff
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
                if tile == 'o':
                    poisoncloud(self,col,row)

    # add sprite classes to Group
    def new(self):
        self.load_data()
        self.randomweather = RandomWeather(self)
        self.cooldown = Timer(self)
        self.mob_timer = Timer(self)
        self.mob_timer.cd = 5
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.speedpotion = pg.sprite.Group()
        self.healthpotion = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.sword = pg.sprite.Group()
        self.poisoncloud = pg.sprite.Group()
        self.teleport = pg.sprite.Group()
        # self.player = Player(self,10,10)
        # self.all_sprites.add(self.player)
        
        #for x in range(10,20):
            #Wall(self,x,5)
        
        # might print walls
        
        # set locations for different sprites
        for row, tiles in enumerate(self.map.data):
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
                if tile == 'o':
                    poisoncloud(self,col,row)
        self.run()

    # runs the game, game won't run without it
    def run(self):
        self.playing = True
        self.surface = self.randomweather.generate_weather()
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # input
            self.events()
            # processing
            self.update()
            # output
            self.draw()

            #weather.generate_weather(self)
            # method; tied to the class
   
    # quits the game when you click the red x
    def quit(self):
        pg.quit()
        sys.exit()

    # method; tied to the class
    def input(self):
        pass

    # updates the position of all sprites on the grid
    def update(self):
        self.cooldown.ticking()
        self.all_sprites.update()

        if self.player.health < 1:
            self.playing = False
        
        if self.player.moneybag == 10:
            for row, tiles in enumerate(self.map.data):
                # print(row)
                for col, tile in enumerate(tiles):
                # print(col)
                    if tile == 't':
                        Teleport(self,col,row)

        if self.player.moneybag == 10:
            if self.player.changem == True:
                if self.current_map <= 3:
                    self.current_map += 1
                    self.change_map(maps[self.current_map])
                elif self.current_map > 3:
                    g.show_end_screen()
        else:
            pass   

    # draws the grid for our game
    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        
        for y in range (0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH,y))

    # sets text settings, ex. font, size, color
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('Times New Roman')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    # paints the background black & draws grid lines
    def draw(self):
        self.screen.blit(self.background_img, self.background_rect)
        # self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        # paints moneybag amount
        self.draw_text(self.screen, str(self.player.moneybag), 35, YELLOW, 1.5, 1)
        # paints a health bar on top of player
        draw_health_bar(self.screen, self.player.rect.x, self.player.rect.y-8, self.player.health)
        # timer
        self.draw_text(self.screen, str(self.cooldown.current_time), 35, RED, 29.5, 1)
        if self.randomweather.weather_number == 0: 
            self.screen.blit(self.surface, (0, 0))
        if self.randomweather.weather_number == 1:
            self.screen.blit(self.surface, (0, 0))
        if self.randomweather.weather_number == 2: 
            self.screen.blit(self.surface, (0, 0))
        if self.randomweather.weather_number == 3:
            self.screen.blit(self.surface, (0, 0))
            # light_screen = pg.surface(30,30)
            # light_screen.set_alpha(200)
            # pg.draw.circle(light_screen, WHITE, (self.player.rect.centerx,self.player.rect.centery), 25)
        # self.draw_text(self.screen, str(self.cooldown.get_countdown()), 35, YELLOW, 4, 1)
        # self.draw_text(self.screen, str(self.cooldown.event_time), 35, YELLOW, 5, 1)

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
            
    # creates a start screen
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play!", 50, WHITE, WIDTH/1000, HEIGHT/1000)
        self.draw_text(self.screen, "Use WASD to control the player.", 50, WHITE, WIDTH/1000, HEIGHT/250)
        self.draw_text(self.screen, "Use the arrow keys to control the storm.", 50, WHITE, WIDTH/1000, HEIGHT/150)
        self.draw_text(self.screen, "Don't die!", 50, WHITE, WIDTH/1000, HEIGHT/100)
        pg.display.flip()
        self.wait_for_key()

    # creates a death screen
    def show_go_screen(self):
        if self.playing == True:
            return
        else: 
            self.screen.fill(BGCOLOR)
            self.draw_text(self.screen, "You died - press any key to play again!", 50, WHITE, WIDTH/1000, HEIGHT/1000)
            pg.display.flip()
            self.wait_for_key()
    
    
    def show_end_screen(self):
        if self.playing == True:
            return
        elif self.current_map > 3:
            self.screen.fill(BGCOLOR)
            self.draw_text(self.screen, "You won - Good Game!", 50, WHITE, WIDTH/1000, HEIGHT/1000)
            pg.display.flip()
            self.wait_for_key()
    
    # waits for pressed key in order to start game
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

# while playing is True the game keeps running
while True:
    g.new()
    g.run()
    g.show_go_screen()