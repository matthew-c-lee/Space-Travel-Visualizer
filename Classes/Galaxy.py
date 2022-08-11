import math
import requests
from xml.etree import ElementTree as ET

from Classes.Star import *

class Galaxy:
    def __init__(self, width, height, num_stars):
        self.stars = generate_stars(width, height, num_stars)
        self.show_star_path = False
        self.show_all_names = False
        self.selected_star = None

        self.destination_x = None
        self.destination_y = None

    def get_stars(self):
        return self.stars

    def set_destination(self, x, y):
        self.destination_x = x
        self.destination_y = y

    def sort_by_closeness(self, ship):
        return self.stars

    def get_selected_star(self):
        return self.selected_star

    # def get_distance_from_destination(self, star):
    #     return math.dist([star.get_x(), star.get_y()], [self.selected_star.get_x(), self.selected_star.get_y()])
    def get_distance_from_destination(self, star):
        return math.dist([star.get_x(), star.get_y()], [self.destination_x, self.destination_y])

# use Sky-Map API to generate stars
def generate_stars(width, height, num_stars):
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
        star = Star(width, height, name)
        lst.append(star)

    return lst



