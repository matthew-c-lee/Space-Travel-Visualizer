
from ast import Num
import pygame

from Classes.Star import *
from Classes.Ship import *
from Classes.Galaxy import *

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
    def draw_stars_path(self, star_list):
        if star_list.show_star_path:
            for i in range(len(star_list) - 1):
                self.draw_star_line(star_list[i], star_list[i+1])

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

    # draw everything. updated each iteration of game loop
    def draw(self, ship, line, star_list):
        self.window.fill(self.BACKGROUND_COLOR)

        self.draw_fuel(ship)

        # test code
        # test_star_list = star_list.list[0:4]
        # self.draw_stars_path(test_star_list)

        # draw line to selected star
        # self.draw_line(line)

        ship.draw(self)
        star_list.draw_stars(self)

        pygame.display.update()


class Line:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y

        self.end_x = end_x
        self.end_y = end_y

        self.line = None

    def get_start_x(self):
        return self.start_x

    def get_start_y(self):
        return self.start_y

    def get_end_x(self):
        return self.end_x

    def get_end_y(self):
        return self.end_y


def list_to_tree(list):
    # treenode = TreeNode()
    pass


def calculate_star_distance(star, ship):
    distance_x = (star.get_x() - ship.get_x())
    distance_y = (star.get_y() - ship.get_y())
    return (abs(distance_x) + abs(distance_y))


def main():
    run = True
    clock = pygame.time.Clock()

    width = 800
    height = 600

    moving = False

    recharging = False

    line = None

    step_x = None
    step_y = None

    draw_info = DrawInfo(width, height)
    # star_list = generate_star_list(draw_info, 50)
    galaxy = Galaxy(draw_info, 50)

    ship = Ship(draw_info)

    # move_x, move_y = ship.x, ship.y

    while run:
        clock.tick(60)

        # Mouse_x, Mouse_y = pygame.mouse.get_pos()

        if recharging and (ship.get_fuel() < ship.get_max_fuel()):
            ship.fuel += 2

        if moving:
            for star in galaxy.stars:
                distance_to_star = calculate_star_distance(ship, star)
                star.set_distance(distance_to_star)

            if abs(move_x - ship.get_x()) < 1 and abs(move_y - ship.get_y()) < 1 or ship.get_fuel() <= 0:
                moving = False
            else:
                ship.move(step_x, step_y)

        draw_info.draw(ship, line, galaxy)
        # show_star_path = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # move ship
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    pass

                # right click
                elif event.button == 3:
                    for star in galaxy.stars:
                        # if they right clicked on a star
                        if has_mouse_hover(star, event.pos):
                            star.show_circle()
                        else:
                            star.hide_circle()

            if event.type == pygame.MOUSEMOTION:
                for star in galaxy.stars:
                    # hovering over star
                    if has_mouse_hover(star, event.pos):
                        star.show_name()

                        distance_to_star = calculate_star_distance(ship, star)
                        star.set_distance(distance_to_star)

                        star.show_distance()
                    else:
                        star.hide_name()
                        star.hide_distance()

            if event.type == pygame.KEYDOWN:

                # show all star names
                if event.key == pygame.K_s:
                    for star in galaxy:
                        distance_to_star = calculate_star_distance(ship, star)
                        star.set_distance(distance_to_star)
                    # toggle
                    galaxy.show_all_names = not galaxy.show_all_names

                elif event.key == pygame.K_SPACE:
                    for star in galaxy.stars:
                        if star.is_selected():
                            move_x, move_y = star.get_x(), star.get_y()

                            # set movement iterations
                            distance_x = (move_x - ship.get_x())
                            distance_y = (move_y - ship.get_y())

                            num_steps = (abs(distance_x) + abs(distance_y)) * 4
                            # num_steps = 45

                            step_x = (distance_x / num_steps)
                            step_y = (distance_y / num_steps)

                            moving = True

                # show star path
                elif event.key == pygame.K_w:
                    galaxy.show_star_path = not galaxy.show_star_path

                # show path
                elif event.key == pygame.K_p:
                    # draw line between you and the star
                    # line = Line()
                    for star in galaxy.stars:
                        if star.is_selected():
                            if line:
                                line = None
                            else:
                                line = Line(ship.get_x(), ship.get_y(),
                                            star.get_x(), star.get_y())

                # recharge fuel
                if event.key == pygame.K_r:
                    closest_star = ship.calculate_closest_star(galaxy)

                    if ship.get_fuel() < ship.get_max_fuel() and calculate_star_distance(ship, closest_star) < 3:
                        recharging = True

            elif event.type == pygame.KEYUP:
                # stop recharging fuel
                if event.key == pygame.K_r:
                    recharging = False

    pygame.quit()


if __name__ == '__main__':
    main()
