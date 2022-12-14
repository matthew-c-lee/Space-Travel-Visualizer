import math
from dis import dis
import pygame
from Classes.Star import *


class Ship:
    MAX_FUEL = 1000

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.fuel = 1000

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_fuel(self):
        return self.fuel

    def add_fuel(self, additional_fuel):
        self.fuel += additional_fuel

    def get_max_fuel(self):
        return self.MAX_FUEL

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move(self, step_x, step_y):
        self.fuel -= 1
        self.set_position(self.x + step_x, self.y + step_y)

    def calculate_closest_star(self, galaxy):
        closest_distance = 1000000
        closest_star = galaxy.stars[0]

        for star in galaxy.stars:
            distance_x = star.get_x() - self.get_x()
            distance_y = star.get_y() - self.get_y()
            distance = abs(distance_x) + abs(distance_y)

            if distance < closest_distance:
                closest_distance = distance
                closest_star = star

        return closest_star
