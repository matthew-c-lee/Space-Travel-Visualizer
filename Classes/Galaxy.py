import requests
from xml.etree import ElementTree as ET

from Classes.Star import *

class Galaxy:
    def __init__(self, width, height, num_stars):
        self.stars = generate_stars(width, height, num_stars)
        self.show_star_path = False
        self.show_all_names = False

    def get_stars(self):
        return self.stars

    def sort_by_closeness(self, ship):
        return self.stars

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

