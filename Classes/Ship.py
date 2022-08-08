import pygame

class Ship:
    def __init__(self, draw_info):
        self.x = draw_info.width // 2
        self.y = draw_info.height // 2

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move(self, move_x, move_y):
        dx, dy = (move_x - self.x, move_y - self.y)
        stepx, stepy = (dx / 45., dy / 45.)
        self.set_position(self.x + stepx, self.y + stepy)

def draw_ship(draw_info, ship):
    pygame.draw.rect(draw_info.window, draw_info.WHITE,
                     (ship.x, ship.y, 15, 15))