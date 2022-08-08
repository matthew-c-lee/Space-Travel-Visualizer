import pygame

class Ship:
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

def draw_ship(draw_info, ship):
    pygame.draw.rect(draw_info.window, draw_info.WHITE,
                     (ship.x, ship.y, 15, 15))