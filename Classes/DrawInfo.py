import pygame
from Classes.Line import *

pygame.init()

class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255

    FONT = pygame.font.SysFont('', 17)
    LARGE_FONT = pygame.font.SysFont('', 22)

    BACKGROUND_COLOR = BLACK

    PAD_X = 25
    PAD_Y = 25

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # self.galaxy = None

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Space Exploration')

    # draw a line

    def draw_line(self, line):
        if line:
            line.line = pygame.draw.line(self.window, self.WHITE,
                                         (line.start_x, line.start_y), (line.end_x, line.end_y))

    # draw line from one star to another
    def draw_star_line(self, star1, star2):
        lineObject = Line(star1.get_x(), star1.get_y(),
                          star2.get_x(), star2.get_y())

        lineObject.line = pygame.draw.line(self.window, self.WHITE,
                                           (lineObject.start_x, lineObject.start_y), (lineObject.end_x, lineObject.end_y))

    # draw entire given star path
    def draw_stars_path(self, galaxy):
        if galaxy.show_star_path:
            for i in range(len(galaxy) - 1):
                self.draw_star_line(galaxy[i], galaxy[i+1])

    # draw fuel indicator
    def draw_fuel(self, ship):
        fuel_outline = pygame.draw.rect(
            self.window, self.WHITE, (25, self.height - 50, 120, 25), width=2)
        fuel_bar = pygame.draw.rect(self.window, self.WHITE, (fuel_outline.left, fuel_outline.top,
                                    fuel_outline.width * (ship.get_fuel()/ship.get_max_fuel()), fuel_outline.height))

        fuel_label = self.LARGE_FONT.render(
            'Solar Energy', 1, self.WHITE)
        self.window.blit(
            fuel_label, (fuel_outline.left, fuel_outline.top - 15))

    def draw_ship(self, ship):
        pygame.draw.rect(self.window, self.WHITE,
                        (ship.get_x(), ship.get_y(), 15, 15))

    def draw_galaxy(self, galaxy, clear_bg=False):
        for star in galaxy.get_stars():
            self.draw_star(star, galaxy.show_all_names)

        if clear_bg:
            pygame.display.update()

    def draw_star(self, star, show_all_star_names):
        star.rect = pygame.draw.rect(self.window, self.WHITE,
                                     (star.x, star.y, 3, 3))

        if star.name_visibility or show_all_star_names:
            star_name = self.FONT.render(star.get_name(), 1, self.WHITE)
            self.window.blit(
                star_name, (star.x - star_name.get_width()/2, star.y - 14))

        if star.circle_visibility:
            pygame.draw.circle(self.window, self.WHITE,
                               (star.x+1, star.y+1), 8, width=1)

        if star.distance_visibility or show_all_star_names:
            distance_label = self.FONT.render(
                f'{str(round(star.distance / 10, 2))} LY', 1, self.WHITE)
            self.window.blit(
                distance_label, (star.x - distance_label.get_width()/2, star.y + 8))

    # draw everything. updated each iteration of game loop
    def draw(self, ship, line, galaxy):
        self.window.fill(self.BACKGROUND_COLOR)

        self.draw_fuel(ship)

        # test code
        # test_star_list = star_list.list[0:4]
        # self.draw_galaxy_path(test_star_list)

        # draw line to selected star
        # self.draw_line(line)

        self.draw_ship(ship)
        self.draw_galaxy(galaxy)

        pygame.display.update()