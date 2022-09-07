"""

This file contains the display page and interactions.
In the state_stor: 0 = empty. 1 = wall. 2 = start. 3 = end.

"""

import pygame
import numpy as np
import astar
import dijkstras as dj
import config

pygame.init()

config.dis.fill(config.blue)
config.dis.fill(config.white, (0, config.dis_height - config.banner_height, config.dis_width, config.banner_height))
config.dis.fill(config.white, (config.square_size, config.square_size, config.dis_width - 2*config.square_size, config.dis_height - config.banner_height - 2*config.square_size))
pygame.display.set_caption('Path Finder')


def round_down(num):  # rounds all values down to just multiples of the pixel size.
    return num - (num % config.square_size)


def draw_path(parents_stor, end):
    colouring = True
    coloured_node = end
    while colouring:
        parent_check = parents_stor[coloured_node[0], coloured_node[1]]
        if parent_check == 0:
            colouring = False
        elif parent_check == 1:
            coloured_node = (coloured_node[0] - 1, coloured_node[1])
        elif parent_check == 2:
            coloured_node = (coloured_node[0], coloured_node[1] + 1)
        elif parent_check == 3:
            coloured_node = (coloured_node[0] + 1, coloured_node[1])
        elif parent_check == 4:
            coloured_node = (coloured_node[0], coloured_node[1] - 1)
        pygame.draw.rect(config.dis, config.orange,
                         [coloured_node[1] * config.square_size, coloured_node[0] * config.square_size,
                          config.square_size, config.square_size])


def displayloop():
    window_close = False
    state_stor = np.zeros((int((config.dis_height - config.banner_height) / config.square_size), int(config.dis_width / config.square_size)))  # an array storing the wall locations.
    for i in range(0, int((config.dis_height - config.banner_height) / config.square_size)):  # creating an outer border to contain the algorithms.
        state_stor[i, 0] = 1
        state_stor[i, int(config.dis_width / config.square_size) - 1] = 1
    for i in range(0, int(config.dis_width / config.square_size)):
        state_stor[0, i] = 1
        state_stor[int((config.dis_height - config.banner_height) / config.square_size) - 1, i] = 1

    current_x, current_y = 0, 0
    current_start_x, current_start_y = 1, 1
    state_stor[current_start_y, current_start_x] = 2
    pygame.draw.rect(config.dis, config.green, [current_start_x * config.square_size, current_start_y * config.square_size, config.square_size, config.square_size])
    current_end_x, current_end_y = int((config.dis_width - 2*config.square_size) / config.square_size), int((config.canvas_height - 2*config.square_size) / config.square_size)
    state_stor[current_end_y, current_end_x] = 3
    pygame.draw.rect(config.dis, config.red, [current_end_x * config.square_size, current_end_y * config.square_size, config.square_size, config.square_size])

    mode_strings = ["Erase", "Draw"]
    mode = 1
    title_font = pygame.font.SysFont('verdana', 20, bold=True)
    info_font = pygame.font.SysFont('verdana', 15)

    mode_text = info_font.render("Mode: " + str(mode_strings[mode]), True, config.red)
    config.dis.blit(mode_text, [config.dis_width - 100, config.canvas_height])

    title_text = title_font.render("Maze Maker", True, config.black)
    config.dis.blit(title_text, [5, config.canvas_height])
    desc_text_1 = info_font.render("Draw a maze, press M to switch modes, R to reset.", True, config.black)
    desc_text_2 = info_font.render("Press D to run Dijkstras algorithm!", True, config.black)
    desc_text_3 = info_font.render("Press A to run the A* algorithm!", True, config.black)
    config.dis.blit(desc_text_1, [5, config.canvas_height + 20])
    config.dis.blit(desc_text_2, [5, config.canvas_height + 40])
    config.dis.blit(desc_text_3, [5, config.canvas_height + 60])

    while not window_close:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    window_close = True
                    config.dis.fill(config.blue)
                    config.dis.fill(config.white, (0, config.dis_height - config.banner_height, config.dis_width, config.banner_height))
                    config.dis.fill(config.white, (config.square_size, config.square_size, config.dis_width - 2 * config.square_size, config.dis_height - config.banner_height - 2 * config.square_size))
                    displayloop()

                if event.key == pygame.K_m:
                    mode = (mode - 1) * -1
                    config.dis.fill(config.white, (config.dis_width - 100, config.canvas_height, 100, 20))
                    mode_text = info_font.render("Mode: " + str(mode_strings[mode]), True, config.red)
                    config.dis.blit(mode_text, [config.dis_width - 100, config.canvas_height])

                if event.key == pygame.K_s:
                    pos = pygame.mouse.get_pos()
                    if int(pos[0] / config.square_size) == current_end_x and int(pos[1] / config.square_size) == current_end_y:
                        pass
                    elif pos[0] > config.square_size and pos[0] < config.dis_width - config.square_size and pos[1] > config.square_size and pos[1] < config.canvas_height - config.square_size:
                        old_start_x, old_start_y = current_start_x, current_start_y
                        current_start_x, current_start_y = int(pos[0] / config.square_size), int(pos[1] / config.square_size)
                        state_stor[old_start_y, old_start_x] = 0
                        state_stor[current_start_y, current_start_x] = 2
                        pygame.draw.rect(config.dis, config.white, [old_start_x * config.square_size, old_start_y * config.square_size, config.square_size, config.square_size])
                        pygame.draw.rect(config.dis, config.green, [round_down(pos[0]), round_down(pos[1]), config.square_size, config.square_size])

                if event.key == pygame.K_e:
                    pos = pygame.mouse.get_pos()
                    if int(pos[0] / config.square_size) == current_start_x and int(pos[1] / config.square_size) == current_start_y:
                        pass
                    elif pos[0] > config.square_size and pos[0] < config.dis_width - config.square_size and pos[1] > config.square_size and pos[1] < config.canvas_height - config.square_size:
                        old_end_x, old_end_y = int(current_end_x), int(current_end_y)
                        current_end_x, current_end_y = int(pos[0] / config.square_size), int(pos[1] / config.square_size)
                        state_stor[old_end_y, old_end_x] = 0
                        state_stor[current_end_y, current_end_x] = 3
                        pygame.draw.rect(config.dis, config.white, [old_end_x * config.square_size, old_end_y * config.square_size, config.square_size, config.square_size])
                        pygame.draw.rect(config.dis, config.red, [round_down(pos[0]), round_down(pos[1]), config.square_size, config.square_size])

                if event.key == pygame.K_d:
                    parents_stor, impossible = dj.dijkstras_main(state_stor)
                    if not impossible:
                        draw_path(parents_stor, (current_end_y, current_end_x))
                        pygame.draw.rect(config.dis, config.green, [current_start_x * config.square_size, current_start_y * config.square_size, config.square_size, config.square_size])
                        pygame.display.update()

                if event.key == pygame.K_a:
                    parents_stor, impossible = astar.astar_main(state_stor)
                    if not impossible:
                        draw_path(parents_stor, (current_end_y, current_end_x))
                        pygame.draw.rect(config.dis, config.green,
                                         [current_start_x * config.square_size, current_start_y * config.square_size,
                                          config.square_size, config.square_size])
                        pygame.display.update()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if int(pos[0] / config.square_size) == current_start_x and int(pos[1] / config.square_size) == current_start_y:
                    pass
                elif int(pos[0] / config.square_size) == current_end_x and int(pos[1] / config.square_size) == current_end_y:
                    pass
                elif pos[0] > config.square_size and pos[0] < config.dis_width - config.square_size and pos[1] > config.square_size and pos[1] < config.canvas_height - config.square_size:
                    change_check_x = int(pos[0] / config.square_size)
                    change_check_y = int(pos[1] / config.square_size)
                    if change_check_x != current_x or change_check_y != current_y:
                        current_x, current_y = change_check_x, change_check_y
                        state_check = state_stor[current_y, current_x]

                        if state_check != mode:
                            state_stor[current_y, current_x] = mode
                            pygame.draw.rect(config.dis, config.colours[mode], [round_down(pos[0]), round_down(pos[1]), config.square_size, config.square_size])

        pygame.display.update()


displayloop()
