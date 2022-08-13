import random
import pygame
import math


class Star:
    def __init__(self, width, height, name=''):
        # add 25 px all around so star names are always visible
        PADDING = 25

        self.x = random.randint(
            PADDING, width - PADDING)
        self.y = random.randint(
            PADDING, height - PADDING)
        self.name = name
        self.name_visibility = False
        self.circle_visibility = False
        self.distance_visibility = False
        self.rect = None

        self.distance_from_ship = 0

    def set_distance_from_ship(self, distance_from_ship):
        self.distance_from_ship = distance_from_ship

    def get_distance_from_ship(self):
        return self.distance_from_ship

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_name(self):
        return self.name

    def is_selected(self):
        return self.circle_visibility

    def show_name(self):
        self.name_visibility = True

    def show_distance(self):
        self.distance_visibility = True

    def hide_distance(self):
        self.distance_visibility = False

    def hide_name(self):
        self.name_visibility = False

    def show_circle(self):
        self.circle_visibility = True

    def hide_circle(self):
        self.circle_visibility = False






    def update_distance_from_ship(self, ship):
        distance_from_ship = calculate_star_distance(self, ship)
        self.distance_from_ship = distance_from_ship



def calculate_star_distance(star, ship):
    return math.dist([star.get_x(), star.get_y()], [ship.get_x(), ship.get_y()])