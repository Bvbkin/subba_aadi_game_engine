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
        print("The current weather is day")
        day_surface = pg.Surface((WIDTH, HEIGHT))
        day_surface.fill(YELLOW)  # Fill the surface with a fog color
        day_surface.set_alpha(128)  # Set the alpha value to make the surface semi-transparent
        #self.screen.blit(fog_surface, (0, 0))  # Blit the fog surface to the screen
        surface = day_surface
        return surface
    
    def rain(self):
        print("The current weather is rain")
        rain_surface = pg.Surface((WIDTH, HEIGHT))
        rain_surface.fill(BLUE)  # Fill the surface with a fog color
        rain_surface.set_alpha(128)  # Set the alpha value to make the surface semi-transparent
        #self.screen.blit(fog_surface, (0, 0))  # Blit the fog surface to the screen
        surface = rain_surface
        return surface
    
    def fog(self):
        print("The current weather is fog")
        fog_surface = pg.Surface((WIDTH, HEIGHT))
        fog_surface.fill(FOG_COLOR)  # Fill the surface with a fog color
        fog_surface.set_alpha(230)  # Set the alpha value to make the surface semi-transparent
        #self.screen.blit(fog_surface, (0, 0))  # Blit the fog surface to the screen
        surface = fog_surface
        return surface
    
    def night(self):
        print("The current weather is night")
        night_surface = pg.Surface((WIDTH, HEIGHT))
        night_surface.fill(BGCOLOR)  # Fill the surface with a fog color
        night_surface.set_alpha(128)  # Set the alpha value to make the surface semi-transparent
        #self.screen.blit(fog_surface, (0, 0))  # Blit the fog surface to the screen
        surface = night_surface
        return surface

    def generate_weather(self):
        
        weather_number = random.randint(0,3)
        # weather_number = 2

        if weather_number == 0:
            surface = self.day()
        if weather_number == 1:
            surface = self.rain()
        if weather_number == 2:
            surface = self.fog()
        if weather_number == 3:
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
