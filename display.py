'''

This file handles displaying the window and user-interactions inside the main programme running function main().
ADD A HANDLER FOR WHEN THE MAZE IS IMPOSSIBLE.
AS WELL AS AFTER A SOLVE HAS BEEN MADE (ONLY RESET SHOULD BE AVAILABLE)
'''

import pygame
import numpy as np
import astar
import dijkstras as dj
import config


# FUNCTIONS
def round_to_grid(num):  
    # rounds coord value down to a multiple of the pixel size, so that pixels can be drawn onto the window.
    return num - (num % config.square_size)


def draw_start(x, y):
    # draws the start node onto the display window.
    pygame.draw.rect(config.dis, config.green, [x * config.square_size, y * config.square_size, config.square_size, config.square_size])


def draw_end(x, y):
    # draws the end node onto the display window.
    pygame.draw.rect(config.dis, config.red, [x * config.square_size, y * config.square_size, config.square_size, config.square_size])


def draw_path(parents_stor, end):
    # draws the solved path onto the window, beginning at the [row, col] position in variable 'end'.
    colouring = True
    coloured_node = end

    while colouring:
        # starting at the end node 'end', identifies the direction of the next path node from 'parents_stor'.
        # colours that node on the screen, then repeats until the source node is identified, indicating the start node has been reached and the entire path is drawn.
        # numbering key: 0 = start node, 1 = move up, 2 = move right, 3 = move down, 4 = move left.
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


# MAIN RUNNING LOOP
def main():
    # FORMAT WINDOW
    config.dis.fill(config.blue)
    config.dis.fill(config.white, (0, config.dis_height - config.banner_height, config.dis_width, config.banner_height))
    config.dis.fill(config.white, (config.square_size, config.square_size, config.dis_width - 2*config.square_size, config.dis_height - config.banner_height - 2*config.square_size))
    pygame.display.set_caption('Path Finder')  # title of window.

    # INITIALISING MAZE ARRAY
    state_stor = np.zeros((int((config.dis_height - config.banner_height) / config.square_size), int(config.dis_width / config.square_size)))
    # In the state_stor: 0 = empty, 1 = wall, 2 = start, 3 = end. Array is arranged as a grid mapping the nodes of the maze.
    # The maze is laid out as [row, col] within the 'state_stor' variable, so need to think about it like (y, x). 
    for i in range(0, int((config.dis_height - config.banner_height) / config.square_size)):  # creating an outer border to contain the algorithms.
        state_stor[i, 0] = 1
        state_stor[i, int(config.dis_width / config.square_size) - 1] = 1
    for i in range(0, int(config.dis_width / config.square_size)):
        state_stor[0, i] = 1
        state_stor[int((config.dis_height - config.banner_height) / config.square_size) - 1, i] = 1

    current_x, current_y = 0, 0  # initialising the clicked node.

    current_start_x, current_start_y = 1, 1  # initialising the start node in top left. 
    state_stor[current_start_y, current_start_x] = 2  # marking this in the state_stor array.
    draw_start(current_start_x, current_start_y)  # drawing the start node.

    current_end_x, current_end_y = int((config.dis_width - 2*config.square_size) / config.square_size), int((config.canvas_height - 2*config.square_size) / config.square_size)  # initialising the end node in the bottom right.
    state_stor[current_end_y, current_end_x] = 3  # marking this in the state_stor array.
    draw_end(current_end_x, current_end_y)  # drawing the end node.

    # ADDING DISPLAY TEXTS
    mode = 1  # initialising mode. 0 = erase, 1 = draw.
    config.add_texts()  # adds texts to display window.

    # USER INTERACTIONS
    window_close = False
    while not window_close:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # window is closed.
                pygame.quit()
                return

            # KEYBOARD INPUTS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 'r' key.
                    # resets the programme.
                    window_close = True  # closes the window.
                    main()  # reruns the main programme loop.

                if event.key == pygame.K_m:  # 'm' key.
                    # changes the mode.
                    mode = (mode - 1) * -1  # this swaps between 0 and 1.
                    config.dis.fill(config.white, (config.dis_width - 100, config.canvas_height, 100, 20))  # pasting new white block to hide old mode text.
                    mode_text = config.info_font.render("Mode: " + str(config.mode_strings[mode]), True, config.red)
                    config.dis.blit(mode_text, [config.dis_width - 100, config.canvas_height])  # drawing new mode text.

                if event.key == pygame.K_s:  # 's' key.
                    # moves the start node to the mouse position.
                    pos = pygame.mouse.get_pos()  # gets raw mouse coords.
                    if int(pos[0] / config.square_size) == current_end_x and int(pos[1] / config.square_size) == current_end_y:
                        pass  # ignores the command if the mouse is positioned on the end node.
                    elif pos[0] > config.square_size and pos[0] < config.dis_width - config.square_size and pos[1] > config.square_size and pos[1] < config.canvas_height - config.square_size:
                        old_start_x, old_start_y = current_start_x, current_start_y  # moves the previous start node position into 'old_start' variables.
                        current_start_x, current_start_y = int(pos[0] / config.square_size), int(pos[1] / config.square_size)  # updates new start node with its integer position in pixel grid.
                        state_stor[old_start_y, old_start_x] = 0  # removes old start node from state_stor.
                        state_stor[current_start_y, current_start_x] = 2  # marks new start node in state_stor.
                        pygame.draw.rect(config.dis, config.white, [old_start_x * config.square_size, old_start_y * config.square_size, config.square_size, config.square_size])  # white pixel over old start node.
                        pygame.draw.rect(config.dis, config.green, [round_to_grid(pos[0]), round_to_grid(pos[1]), config.square_size, config.square_size])  # green pixel over new start node.

                if event.key == pygame.K_e:  # 'e' key.
                    # moves the end node to the mouse position.
                    pos = pygame.mouse.get_pos()  # gets raw mouse coords.
                    if int(pos[0] / config.square_size) == current_start_x and int(pos[1] / config.square_size) == current_start_y:
                        pass  # ignores the command if the mouse is positioned on the start node.
                    elif pos[0] > config.square_size and pos[0] < config.dis_width - config.square_size and pos[1] > config.square_size and pos[1] < config.canvas_height - config.square_size:
                        old_end_x, old_end_y = int(current_end_x), int(current_end_y)  # moves the previous end node position into 'old_end' variables.
                        current_end_x, current_end_y = int(pos[0] / config.square_size), int(pos[1] / config.square_size)  # updates the new end node with its integer position in pixel grid.
                        state_stor[old_end_y, old_end_x] = 0  # removes old end node from state_stor.
                        state_stor[current_end_y, current_end_x] = 3  # marks new end node in state_stor.
                        pygame.draw.rect(config.dis, config.white, [old_end_x * config.square_size, old_end_y * config.square_size, config.square_size, config.square_size])  # white pixel over old end node.
                        pygame.draw.rect(config.dis, config.red, [round_to_grid(pos[0]), round_to_grid(pos[1]), config.square_size, config.square_size])  # green pixel over new end node.

                if event.key == pygame.K_d:  # 'd' key.
                    # solves the maze using Dijkstras algorithm.
                    parents_stor, impossible = dj.dijkstras_main(state_stor)  # runs the algorithm.
                    if impossible:
                        config.impossible_text()
                    if not impossible:
                        draw_path(parents_stor, (current_end_y, current_end_x))  # draws solved path.
                        pygame.draw.rect(config.dis, config.green, [current_start_x * config.square_size, current_start_y * config.square_size, config.square_size, config.square_size])  # redraws start node.
                        config.solved_text()
                    pygame.display.update()  # pushes these updates onto the window.

                    end_screen = True
                    while end_screen == True:
                        for event in pygame.event.get():  # reduces input options to quitting or resetting.
                            if event.type == pygame.QUIT:  # window is closed.
                                pygame.quit()
                                return
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:  # 'r' key.
                                    # resets the programme.
                                    window_close = True  # closes the window.
                                    main()  # reruns the main programme loop.

                if event.key == pygame.K_a:  # 'a' key.
                    parents_stor, impossible = astar.astar_main(state_stor)  # runs the algorithm.
                    if impossible:
                        config.impossible_text()
                    if not impossible:
                        draw_path(parents_stor, (current_end_y, current_end_x))  # draws solved path.
                        pygame.draw.rect(config.dis, config.green, [current_start_x * config.square_size, current_start_y * config.square_size, config.square_size, config.square_size])  # redraws start node.
                        config.solved_text()
                    pygame.display.update()  # pushes these updates onto the window.

                    end_screen = True
                    while end_screen == True:
                        for event in pygame.event.get():  # reduces input options to quitting or resetting.
                            if event.type == pygame.QUIT:  # window is closed.
                                pygame.quit()
                                return
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:  # 'r' key.
                                    # resets the programme.
                                    window_close = True  # closes the window.
                                    main()  # reruns the main programme loop.

            # MOUSE INPUTS
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()  # gets coords of mouse position.
                if int(pos[0] / config.square_size) == current_start_x and int(pos[1] / config.square_size) == current_start_y:
                    pass  # ignore command if the start node is clicked.
                elif int(pos[0] / config.square_size) == current_end_x and int(pos[1] / config.square_size) == current_end_y:
                    pass  # ignore command if the end node is clicked.
                elif pos[0] > config.square_size and pos[0] < config.dis_width - config.square_size and pos[1] > config.square_size and pos[1] < config.canvas_height - config.square_size:  # checks if clicked node is within maze boundaries.
                    change_check_x = int(pos[0] / config.square_size)
                    change_check_y = int(pos[1] / config.square_size)
                    if change_check_x != current_x or change_check_y != current_y:  # only runs changes if clicked node is different to previously clicked node.
                        current_x, current_y = change_check_x, change_check_y  # clicked node becomes currently clicked node.
                        state_check = state_stor[current_y, current_x]  # checks the current state of the clicked node.

                        if state_check != mode:  # checks if current state of node is different to current mode.
                            state_stor[current_y, current_x] = mode  # changes node to mode state.
                            pygame.draw.rect(config.dis, config.mode_colours[mode], [round_to_grid(pos[0]), round_to_grid(pos[1]), config.square_size, config.square_size])  # draws new node state onto display window.

        pygame.display.update()  # pushes any updates to display window every loop.


main()  # running the main programme loop.
