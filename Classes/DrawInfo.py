import pygame

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
        self.action_button = ActionButton()
        # self.galaxy = None

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Space Exploration')

    # draw line from one star to another
    def draw_line(self, start_x, start_y, end_x, end_y):
        pygame.draw.line(self.window, self.WHITE,
                         [start_x, start_y], [end_x, end_y])

    def draw_star_line(self, start_star, end_star):
        pygame.draw.line(self.window, self.WHITE,
                         [start_star.get_x(), start_star.get_y()], [end_star.get_x(), end_star.get_y()])

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
        # triangle shape
        pygame.draw.polygon(self.window, self.WHITE,
                            ((ship.get_x(), ship.get_y()), (ship.get_x()+5, ship.get_y()+10), (ship.get_x()+10, ship.get_y())))

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
                f'{str(round(star.get_distance_from_ship() / 10, 2))} LY', 1, self.WHITE)
            self.window.blit(
                distance_label, (star.x - distance_label.get_width()/2, star.y + 8))

    def draw_best_path(self, best_path, ship):
        if best_path:
            self.draw_line(ship.get_x(), ship.get_y(),
                           best_path[0].get_x(), best_path[0].get_y())

            for i in range(len(best_path) - 1):
                start_star = best_path[i]
                end_star = best_path[i+1]
                self.draw_line(start_star.get_x(), start_star.get_y(),
                               end_star.get_x(), end_star.get_y())
                # self.draw_star_line(best_path[i], best_path[i+1])
            # draw everything. updated each iteration of game loop

    def draw_tutorial(self):
        tutorial_label = self.LARGE_FONT.render(
            'Left Click - Select Star  |  Space - Go to Star  |  V - Show Path  |  R - Refuel', 1, self.WHITE)
        self.window.blit(
            tutorial_label, (10, 10))

    def draw_action_button(self):
        fuel_label = self.LARGE_FONT.render(
            self.action_button.message, 1, self.WHITE)

        padding = 10

        button_width = fuel_label.get_width()
        button_height = 40

        self.action_button.rect = pygame.draw.rect(
            self.window, self.WHITE, (self.width - button_width - 50, self.height - 65, button_width + padding*2, button_height), width=2)

        self.window.blit(
            fuel_label, (self.action_button.rect.left + padding, self.action_button.rect.bottom - 25))

    def draw(self, ship, best_path, galaxy, action_message):
        self.window.fill(self.BACKGROUND_COLOR)

        self.draw_fuel(ship)

        self.action_button.message = action_message
        # self.draw_action_button()

        self.draw_tutorial()

        # draw line to selected star
        self.draw_best_path(best_path, ship)

        self.draw_ship(ship)
        self.draw_galaxy(galaxy)

        pygame.display.update()


class ActionButton:
    def __init__(self):
        self.rect = None
        self.message = '          '
