
import pygame

from Classes.Star import *
from Classes.Ship import *
from Classes.Galaxy import *
from Classes.DrawInfo import *

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

    draw_info = DrawInfo(width, height)

    moving = False

    is_recharging = False

    line = None

    step_x = None
    step_y = None

    # star_list = generate_star_list(draw_info, 50)
    galaxy = Galaxy(width, height, 50)
        
    ship = Ship(draw_info.width // 2, draw_info.height // 2)

    # move_x, move_y = ship.x, ship.y

    while run:
        clock.tick(60)

        # Mouse_x, Mouse_y = pygame.mouse.get_pos()
        has_max_fuel = ship.get_fuel() >= ship.get_max_fuel()
        if is_recharging and not has_max_fuel:
            ship.fuel += 2

        if moving:
            for star in galaxy.stars:
                distance_to_star = calculate_star_distance(ship, star)
                star.set_distance(distance_to_star)

            has_no_fuel = ship.get_fuel() <= 0
            has_reached_destination = abs(move_x - ship.get_x()) < 1 and abs(move_y - ship.get_y()) < 1
            if has_reached_destination or has_no_fuel:
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
                    for star in galaxy.get_stars():
                        # if they right clicked on a star
                        if star.has_mouse_hover(event.pos):
                            star.show_circle()
                        else:
                            star.hide_circle()

            if event.type == pygame.MOUSEMOTION:
                for star in galaxy.stars:
                    # hovering over star
                    if star.has_mouse_hover(event.pos):
                        # update distance info
                        distance_to_star = calculate_star_distance(ship, star)
                        star.set_distance(distance_to_star)

                        star.show_name()
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

                    is_close_enough = calculate_star_distance(ship, closest_star) < 3
                    has_max_fuel = ship.get_fuel() >= ship.get_max_fuel()
                    if not has_max_fuel and is_close_enough:
                        is_recharging = True

            elif event.type == pygame.KEYUP:
                # stop recharging fuel
                if event.key == pygame.K_r:
                    is_recharging = False

    pygame.quit()


if __name__ == '__main__':
    main()
