
import pygame

from Classes.Star import *
from Classes.Ship import *

pygame.init()


class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255

    FONT = pygame.font.SysFont('', 15)

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

    draw_line(draw_info, line)

    draw_ship(draw_info, ship)
    draw_stars(draw_info, show_all_star_names)

    pygame.display.update()


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

    move_x, move_y = ship.x, ship.y

    while run:
        clock.tick(60)

        Mouse_x, Mouse_y = pygame.mouse.get_pos()

        if moving:
            ship.move(move_x, move_y)

            if abs(move_x - ship.x) < 5 and abs(move_y - ship.y) < 5:
                moving = False
                # print('done moving')

        draw(draw_info, ship, show_all_star_names, line)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # move ship
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    for star in draw_info.star_list:
                        if star.is_selected():
                            move_x, move_y = star.get_x(), star.get_y()
                            moving = True

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
                    if has_mouse_hover(star, event.pos):
                        star.show_name()
                    else:
                        star.hide_name()

            if event.type != pygame.KEYDOWN:
                continue

            # show all star names
            if event.key == pygame.K_s:
                # toggle
                show_all_star_names = not show_all_star_names

            # show path
            elif event.key == pygame.K_p:
                # draw line between you and the star
                # line = Line()
                line = None
                for star in draw_info.star_list:
                    if star.is_selected():
                        line = Line(ship.x, ship.y, star.get_x(), star.get_y())

    pygame.quit()


if __name__ == '__main__':
    main()
