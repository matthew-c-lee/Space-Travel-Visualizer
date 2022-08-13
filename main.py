
from tabnanny import check
import pygame

import math

from Classes.Star import *
from Classes.Ship import *
from Classes.Galaxy import *
from Classes.DrawInfo import *


def find_best_path(galaxy, ship):
    best_path = []

    current_x, current_y = ship.get_x(), ship.get_y()

    galaxy.set_destination(current_x, current_y)

    last_star_in_path = None
    # run until it reaches the final star
    while(last_star_in_path != galaxy.get_selected_star()):
        sorted_list = sorted(
            galaxy.get_stars(), key=galaxy.get_distance_from_destination)

        # loop through stars until it finds a star that will bring it closer to
        # the destination, then break
        for star in sorted_list:
            if is_closer_to_destination(current_x, current_y, star, galaxy.get_selected_star()):
                best_path.append(star)
                last_star_in_path = star

                # update coordinates
                current_x, current_y = star.get_x(), star.get_y()
                galaxy.set_destination(current_x, current_y)
                break

    return best_path


def is_closer_to_destination(current_x, current_y, checking_star, destination_star):
    to_star_distance = math.dist(
        [destination_star.get_x(), destination_star.get_y()], [current_x, current_y])
    star_to_destination_distance = math.dist([destination_star.get_x(
    ), destination_star.get_y()], [checking_star.get_x(), checking_star.get_y()])

    return star_to_destination_distance < to_star_distance


def has_mouse_hover(shape, mouse):
    # if hovering, return true
    return shape.collidepoint(mouse)


def main():
    run = True
    clock = pygame.time.Clock()

    width = 800
    height = 700

    moving = False
    is_recharging = False

    best_path = None

    step_x = None
    step_y = None

    action_message = '                   '

    action_button = ActionButton()
    draw_info = DrawInfo(width, height)
    galaxy = Galaxy(width, height - 100, 50)
    ship = Ship(draw_info.width // 2, draw_info.height // 2)

    while run:
        clock.tick(60)
        draw_info.draw(ship, best_path, galaxy, action_message)

        has_max_fuel = ship.get_fuel() >= ship.get_max_fuel()
        if is_recharging and not has_max_fuel:
            ship.add_fuel(2)

        has_no_fuel = ship.get_fuel() <= 0
        if has_no_fuel:
            action_message = 'Self Destruct'
        elif galaxy.get_selected_star():
            action_message = 'Go to Star'

        if moving:
            for star in galaxy.get_stars():
                star.update_distance_from_ship(ship)

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
                    for star in galaxy.get_stars():
                        # if they right clicked on a star
                        if has_mouse_hover(star.rect, event.pos):
                            galaxy.set_selected_star(star)
                            star.show_circle()
                        else:
                            # galaxy.set_selected_star(None)
                            star.hide_circle()

            elif event.type == pygame.MOUSEMOTION:
                for star in galaxy.get_stars():
                    # hovering over star
                    if has_mouse_hover(star.rect, event.pos):
                        # update distance info
                        star.update_distance_from_ship(ship)

                        star.show_name()
                        star.show_distance()

                        # clicked_action = has_mouse_hover(draw_info.action_button.rect, event.pos)
                        # clicked_go_to_star = clicked_action and draw_info.action_button.message == 'Go to Star'
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
                for star in galaxy.get_stars():
                    star.update_distance_from_ship(ship)

                # toggle
                galaxy.show_all_names = not galaxy.show_all_names

            elif event.key == pygame.K_SPACE:
                for star in galaxy.get_stars():
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
                    best_path = find_best_path(galaxy, ship)

    pygame.quit()


if __name__ == '__main__':
    main()
