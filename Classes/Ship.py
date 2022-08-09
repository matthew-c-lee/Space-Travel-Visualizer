from dis import dis
import pygame
from Classes.Star import *

class Ship:
    MAX_FUEL = 1000

    def __init__(self, draw_info):
        self.x = draw_info.width // 2
        self.y = draw_info.height // 2

        self.fuel = 1000

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_fuel(self):
        return self.fuel

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move(self, step_x, step_y):
        self.fuel -= 1
        self.set_position(self.x + step_x, self.y + step_y)

    def calculate_closest_star(self, star_list):
        closest_distance = 1000000
        closest_star = star_list[0]
        
        for star in star_list:
            distance_x = star.get_x() - self.get_x()
            distance_y = star.get_y() - self.get_y()
            distance = abs(distance_x) + abs(distance_y)

            if distance < closest_distance:
                closest_distance = distance
                closest_star = star

        return closest_star

def draw_ship(draw_info, ship):
    pygame.draw.rect(draw_info.window, draw_info.WHITE,
                     (ship.x, ship.y, 15, 15))