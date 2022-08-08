
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
        

def draw(draw_info, ship, show_all_star_names):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

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

        draw(draw_info, ship, show_all_star_names)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # move ship
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    moving = True
                    move_x = Mouse_x
                    move_y = Mouse_y

                # right click
                elif event.button == 3:
                    for star in draw_info.star_list:
                        # if they right clicked on a star
                        if has_mouse_hover(star, event.pos):
                            move_x, move_y = star.get_x(), star.get_y()
                            moving = True

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

    pygame.quit()


if __name__ == '__main__':
    main()
