import random
import pygame


class Star:
    def __init__(self, draw_info, name=''):
        self.x = random.randint(
            draw_info.PAD_X, draw_info.width - draw_info.PAD_X)
        self.y = random.randint(
            draw_info.PAD_Y, draw_info.height - draw_info.PAD_Y)
        self.name = name
        self.name_visibility = False
        self.circle_visibility = False
        self.distance_visibility = False
        self.rect = None

        self.distance = 0

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

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

    def show_distance(self):
        self.distance_visibility = True

    def hide_distance(self):
        self.distance_visibility = False

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
                star_name, (self.x - star_name.get_width()/2, self.y - 14))

        if self.circle_visibility:
            pygame.draw.circle(draw_info.window, draw_info.WHITE,
                               (self.x+1, self.y+1), 8, width=1)

        if self.distance_visibility or show_all_star_names:
            distance_label = draw_info.FONT.render(
                f'{str(round(self.distance / 10, 2))} LY', 1, draw_info.WHITE)
            draw_info.window.blit(
                distance_label, (self.x - distance_label.get_width()/2, self.y + 8))


def has_mouse_hover(star, mouse):
    # if hovering, return true
    return star.rect.collidepoint(mouse)
