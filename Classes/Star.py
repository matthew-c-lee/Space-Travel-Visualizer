import random
import pygame
import requests
from xml.etree import ElementTree as ET


class Star:
    def __init__(self, draw_info, name=''):
        self.x = random.randint(
            draw_info.PAD_X, draw_info.width - draw_info.PAD_X)
        self.y = random.randint(
            draw_info.PAD_Y, draw_info.height - draw_info.PAD_Y)
        self.name = name
        self.name_visibility = False
        self.circle_visibility = False
        self.rect = None

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

    def hide_name(self):
        self.name_visibility = False

    def show_circle(self):
        self.circle_visibility = True

    def hide_circle(self):
        self.circle_visibility = False

    def draw(self, draw_info, show_all_star_names):
        self.rect = pygame.draw.rect(draw_info.window, draw_info.WHITE,
                                     (self.x, self.y, 3, 3))

        if self.name_visibility or show_all_star_names:
            star_name = draw_info.FONT.render(self.name, 1, draw_info.WHITE)
            draw_info.window.blit(
                star_name, (self.x - star_name.get_width()/2, self.y - 12))

        if self.circle_visibility:
            pygame.draw.circle(draw_info.window, draw_info.WHITE,
                               (self.x+1, self.y+1), 8, width=1)


def has_mouse_hover(star, mouse):
    # if hovering, return true
    return star.rect.collidepoint(mouse)


# use Sky-Map API to generate stars
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

    star_data = tree.findall('star')

    lst = []
    for star in star_data:
        name = star.find('catId').text
        star = Star(draw_info, name)
        lst.append(star)

    return lst


def draw_stars(draw_info, show_all_star_names, clear_bg=False):
    stars = draw_info.star_list

    for star in stars:
        star.draw(draw_info, show_all_star_names)

    if clear_bg:
        pygame.display.update()
