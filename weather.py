import pygame as pg
import random
from settings import *

class RandomWeather: 
    def __init__(self, game):
        self.game = game
        self.current_weather = None

    def day():
        print("The current weather is day")
        pass
    def rain():
        print("The current weather is rain")

        pass
    def fog():
        print("The current weather is fog")
        fog_surface = pg.Surface((WIDTH, HEIGHT))
        fog_surface.fill(FOG_COLOR)
        fog_surface.set_alpha(128)  # Set transparency
    def night():
        print("The current weather is night")
        pass

    def generate_weather(self):
        self.weather_types = {
            0: self.day(),
            1: self.rain(),
            2: self.fog(),
            4: self.night()
        }
        # self.current_weather = random.choice(self.weather_types)
        self.current_weather = self.weather_types[2]
        return self.current_weather
