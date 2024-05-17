import pygame as pg
import random
from settings import *
from sprites import *

class RandomWeather: 
    def __init__(self, game):
        self.game = game
        # self.current_weather = None
        # self.surface = None

    def day(self):
        '''
        print("It is daytime!")
        surface  = None
        return surface
        '''
        day_surface = pg.Surface((WIDTH, HEIGHT))
        day_surface.fill(YELLOW)  # Fill the surface with a fog color
        day_surface.set_alpha(0)  # Set the alpha value to make the surface semi-transparent
        #self.screen.blit(fog_surface, (0, 0))  # Blit the fog surface to the screen
        surface = day_surface
        return surface
        
    def rain(self):
        print("It started raining!")
        # self.x = x
        # self.y = y
        self.speed = 5
        self.size = 2
        rain_surface = pg.Surface((WIDTH, HEIGHT))
        rain_surface.fill(BLUE)  # Fill the surface with a fog color
        rain_surface.set_alpha(128)  # Set the alpha value to make the surface semi-transparent

        surface = rain_surface
        return surface
    
    def fog(self):
        print("It got foggy!")
        fog_surface = pg.Surface((WIDTH, HEIGHT))
        fog_surface.fill(FOG_COLOR)  # Fill the surface with a fog color
        fog_surface.set_alpha(230)  # Set the alpha value to make the surface semi-transparent
        #self.screen.blit(fog_surface, (0, 0))  # Blit the fog surface to the screen
        surface = fog_surface
        return surface
    
    def night(self):
        
        print("It turned night!")
        night_surface = pg.Surface((WIDTH, HEIGHT))
        night_surface.fill(BGCOLOR)  # Fill the surface with a fog color
        night_surface.set_alpha(200)  # Set the alpha value to make the surface semi-transparent
        #self.screen.blit(fog_surface, (0, 0))  # Blit the fog surface to the screen
        surface = night_surface
        return surface
    '''
    def light_bubble(self,x, y, radius):
        print("Light bubble appeared!")
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255,255,255)
    '''
    def generate_weather(self):
        
        self.weather_number = random.randint(0,3)
        # self.weather_number = 0

        if self.weather_number == 0:
            surface = self.day()
        if self.weather_number == 1:
            surface = self.rain()
        if self.weather_number == 2:
            surface = self.fog()
        if self.weather_number == 3:
            surface = self.night()

        '''
        self.weather_types = {
            0: self.day(),
            1: self.rain(),
            2: self.fog(),
            3: self.night()
        }
        '''
        # self.current_weather = self.weather_types[random.randint(0,3)]
        # self.current_weather = self.weather_types[2]
        return surface
    
class LightBubble:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 255, 255)  # White color for the light bubble



