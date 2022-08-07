import requests
from xml.etree import ElementTree as ET
import pygame
import random

pygame.init()


class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255

    FONT = pygame.font.SysFont('', 15)

    BACKGROUND_COLOR = BLACK

    X_PAD = 25
    Y_PAD = 25

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.lst = None

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Space Exploration')

    def set_list(self, lst):
        self.lst = lst


class Star:
    def __init__(self, draw_info, name=''):
        self.pos_x = random.randint(draw_info.X_PAD, draw_info.width - draw_info.X_PAD)
        self.pos_y = random.randint(draw_info.Y_PAD, draw_info.height - draw_info.Y_PAD)
        self.name = name


def generate_star_list(draw_info, num_stars):
    params = {
        'ra': 40,
        'de': 100,
        'angle': 90,
        'max_stars': num_stars,
        'max_vmag': 100,
    }

    response = requests.get("https://server2.sky-map.org/getstars.jsp", params)

    tree = ET.fromstring(response.content)

    stars = tree.findall('star')

    lst = []
    for star in stars:
        name = star.find('catId').text
        star = Star(draw_info, name)
        lst.append(star)

    return lst


def draw_stars(draw_info, show_stars, clear_bg=False):
    stars = draw_info.lst

    for star in stars:
        pygame.draw.rect(draw_info.window, draw_info.WHITE,
                         (star.pos_x, star.pos_y, 3, 3))

        if show_stars:
            star_name = draw_info.FONT.render(star.name, 1, draw_info.WHITE)
            draw_info.window.blit(
                star_name, (star.pos_x - star_name.get_width()/2, star.pos_y - 12))

    if clear_bg:
        pygame.display.update()


def draw(draw_info, show_stars):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    draw_stars(draw_info, show_stars)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    width = 800
    height = 600

    show_stars = False

    draw_info = DrawInfo(width, height)
    draw_info.set_list(generate_star_list(draw_info, 50))

    draw(draw_info, show_stars)

    while run:
        clock.tick(60)

        draw(draw_info, show_stars)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            # show star names
            if event.key == pygame.K_s:
                # toggle boolean
                show_stars = not show_stars

    pygame.quit()


if __name__ == '__main__':
    main()
