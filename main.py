
from tabnanny import check
import pygame

import math

from Classes.Star import *
from Classes.Ship import *
from Classes.Galaxy import *
from Classes.DrawInfo import *


def list_to_tree(list):
    # treenode = TreeNode()
    pass


def calculate_star_distance(star, ship):
    return math.dist([star.get_x(), star.get_y()], [ship.get_x(), ship.get_y()])


def main():
    run = True
    clock = pygame.time.Clock()

    width = 800
    height = 600

    moving = False
    is_recharging = False

    best_path = None

    step_x = None
    step_y = None

    draw_info = DrawInfo(width, height)
    galaxy = Galaxy(width, height, 50)
    ship = Ship(draw_info.width // 2, draw_info.height // 2)

    while run:
        clock.tick(60)
        draw_info.draw(ship, best_path, galaxy)

        has_max_fuel = ship.get_fuel() >= ship.get_max_fuel()
        if is_recharging and not has_max_fuel:
            ship.fuel += 2

        if moving:
            for star in galaxy.stars:
                distance_from_ship = calculate_star_distance(ship, star)
                star.set_distance_from_ship(distance_from_ship)

            has_no_fuel = ship.get_fuel() <= 0
            has_reached_destination = abs(
                move_x - ship.get_x()) < 1 and abs(move_y - ship.get_y()) < 1
            if has_reached_destination or has_no_fuel:
                moving = False
            else:
                ship.move(step_x, step_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                continue

            # move ship
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    pass

                # right click
                elif event.button == 3:
                    for star in galaxy.get_stars():
                        # if they right clicked on a star
                        if star.has_mouse_hover(event.pos):
                            galaxy.selected_star = star
                            print(star)
                            star.show_circle()
                        else:
                            star.hide_circle()

            elif event.type == pygame.MOUSEMOTION:
                for star in galaxy.stars:
                    # hovering over star
                    if star.has_mouse_hover(event.pos):
                        # update distance info
                        distance_from_ship = calculate_star_distance(ship, star)
                        star.set_distance_from_ship(distance_from_ship)

                        star.show_name()
                        star.show_distance()
                    else:
                        star.hide_name()
                        star.hide_distance()

            elif event.type == pygame.KEYUP:
                # stop recharging fuel
                if event.key == pygame.K_r:
                    is_recharging = False

            # if no keys are down, skip rest of the code in the loop
            elif event.type != pygame.KEYDOWN:
                continue

            # show all star names
            elif event.key == pygame.K_s:
                for star in galaxy.stars:
                    distance_from_ship = calculate_star_distance(ship, star)
                    star.set_distance_from_ship(distance_from_ship)
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
            elif event.key == pygame.K_r:
                closest_star = ship.calculate_closest_star(galaxy)

                is_close_enough = calculate_star_distance(
                    ship, closest_star) < 3
                has_max_fuel = ship.get_fuel() >= ship.get_max_fuel()
                if not has_max_fuel and is_close_enough:
                    is_recharging = True

            # sorted stars printed out
            elif event.key == pygame.K_v:
                best_path = []

                if galaxy.get_selected_star():
                    current_x, current_y = ship.get_x(), ship.get_y()

                    galaxy.set_destination(current_x, current_y)
    
                    # while(idek)
                    last_index_check = 0
                    while(last_index_check != galaxy.get_selected_star()):
                        sorted_list = sorted(galaxy.stars, key=galaxy.get_distance_from_destination)

                        for star in sorted_list:
                            if is_positive_distance(current_x, current_y, star, galaxy.get_selected_star()):
                                best_path.append(star)
                                last_index_check = star

                                # update coordinates
                                current_x, current_y = star.get_x(), star.get_y()
                                galaxy.set_destination(current_x, current_y)

                                break
            
    pygame.quit()


def is_positive_distance(current_x, current_y, checking_star, destination_star):
    total_ship_to_star_distance = math.dist([destination_star.get_x(), destination_star.get_y()], [current_x, current_y])
    total_stars_distance = math.dist([destination_star.get_x(), destination_star.get_y()], [checking_star.get_x(), checking_star.get_y()])

    is_closer_than_ship = total_stars_distance < total_ship_to_star_distance
    return is_closer_than_ship


    

if __name__ == '__main__':
    main()