import pygame as pg
import random
from settings import *

class RandomWeather: 
    def __init__(self, game):
        self.game = game
        self.weather_types = {
            0: self.day(),
            1: self.rain(),
            2: self.fog(),
            3: self.snow(),
            4: self.night()
        }
        self.current_weather = None

    def day():
        pass
    def rain():
        pass
    def fog():
        fog_surface = pg.Surface((WIDTH, HEIGHT))
        fog_surface.fill(FOG_COLOR)
        fog_surface.set_alpha(128)  # Set transparency
    def snow():
        pass
    def night():
        pass

    def generate_weather(self):
        # self.current_weather = random.choice(self.weather_types)
        self.current_weather = self.weather_types(2)
        return self.current_weather
