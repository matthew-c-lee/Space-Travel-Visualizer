
from ast import Num
import pygame

from Classes.Star import *
from Classes.Ship import *

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
        self.star_list = None

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Space Exploration')

    def set_list(self, star_list):
        self.star_list = star_list


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


def draw_line(draw_info, line):
    if line:
        line.line = pygame.draw.line(draw_info.window, draw_info.WHITE,
                                     (line.start_x, line.start_y), (line.end_x, line.end_y))


def draw(draw_info, ship, show_all_star_names, line):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    fuel_outline = pygame.draw.rect(draw_info.window, draw_info.WHITE, (25, draw_info.height - 50, 120, 25), width=2)
    fuel_bar = pygame.draw.rect(draw_info.window, draw_info.WHITE, (fuel_outline.left, fuel_outline.top, fuel_outline.width * (ship.get_fuel()/ship.MAX_FUEL), fuel_outline.height))


    fuel_label = draw_info.LARGE_FONT.render('Solar Energy', 1, draw_info.WHITE)
    draw_info.window.blit(fuel_label, (fuel_outline.left, fuel_outline.top - 15))



    draw_line(draw_info, line)

    draw_ship(draw_info, ship)
    draw_stars(draw_info, show_all_star_names)


    pygame.display.update()

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

    show_all_star_names = False

    line = None

    draw_info = DrawInfo(width, height)
    draw_info.set_list(generate_star_list(draw_info, 50))

    ship = Ship(draw_info)

    recharging = False

    # move_x, move_y = ship.x, ship.y
    step_x = None 
    step_y = None

    while run:
        clock.tick(60)

        # Mouse_x, Mouse_y = pygame.mouse.get_pos()

        if recharging and (ship.get_fuel() < ship.MAX_FUEL):
            ship.fuel += 2

        if moving:
            for star in draw_info.star_list:
                distance_to_star = calculate_star_distance(ship, star)
                star.set_distance(distance_to_star)

            if abs(move_x - ship.get_x()) < 1 and abs(move_y - ship.get_y()) < 1 or ship.get_fuel() <= 0:
                moving = False
            else:
                ship.move(step_x, step_y)


        draw(draw_info, ship, show_all_star_names, line)

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
                    for star in draw_info.star_list:
                        # if they right clicked on a star
                        if has_mouse_hover(star, event.pos):
                            star.show_circle()
                        else:
                            star.hide_circle()

            if event.type == pygame.MOUSEMOTION:
                for star in draw_info.star_list:
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
                    for star in draw_info.star_list:
                        distance_to_star = calculate_star_distance(ship, star)
                        star.set_distance(distance_to_star)
                    # toggle
                    show_all_star_names = not show_all_star_names

                elif event.key == pygame.K_SPACE:
                    for star in draw_info.star_list:
                        if star.is_selected():
                            move_x, move_y = star.get_x(), star.get_y()

                            # set movement iterations
                            distance_x = (move_x - ship.get_x())
                            distance_y = (move_y - ship.get_y())

                            num_steps = (abs(distance_x) + abs(distance_y)) * 8
                            # num_steps = 45

                            step_x = (distance_x / num_steps)
                            step_y = (distance_y / num_steps)

                            moving = True

                # show path
                elif event.key == pygame.K_p:
                    # draw line between you and the star
                    # line = Line()
                    for star in draw_info.star_list:
                        if star.is_selected():
                            if line:
                                line = None
                            else:
                                line = Line(ship.get_x(), ship.get_y(),
                                            star.get_x(), star.get_y())


                # recharge fuel
                if event.key == pygame.K_r:
                    closest_star = ship.calculate_closest_star(draw_info.star_list)

                    if ship.get_fuel() < ship.MAX_FUEL and calculate_star_distance(ship, closest_star) < 3: 
                        recharging = True

            elif event.type == pygame.KEYUP:    
                # stop recharging fuel
                if event.key == pygame.K_r:
                    recharging = False

    pygame.quit()


if __name__ == '__main__':
    main()
