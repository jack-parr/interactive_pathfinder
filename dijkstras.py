"""

This file contains dijkstras algorithm based on an array of the maze.

"""

import numpy as np
import pygame
import time
import config


def initiate(board):
    board_dims = np.shape(board)
    min_dis_stor = np.full(board_dims, 9999)
    parent_node_stor = np.zeros(board_dims, int)
    unvisited = {}
    for row in range(0, board_dims[0]):
        for col in range(0, board_dims[1]):
            state_check = board[row, col]
            if state_check != 1:
                unvisited.update({(row, col): 9999})
                if state_check == 2:
                    unvisited.update({(row, col): 0})
                    min_dis_stor[row, col] = 0

    return min_dis_stor, parent_node_stor, unvisited


def check_up(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited):
    end_check = False
    try:
        up_node = maze_array[selected_node[0] - 1, selected_node[1]]
        if up_node != 1:
            new_dis = min_dis_stor[selected_node[0], selected_node[1]] + 1
            if new_dis < min_dis_stor[selected_node[0] - 1, selected_node[1]]:
                min_dis_stor[selected_node[0] - 1, selected_node[1]] = new_dis
                parent_node_stor[selected_node[0] - 1, selected_node[1]] = 3
                unvisited.update({(selected_node[0] - 1, selected_node[1]): new_dis})
            if up_node == 3:
                end_check = True
    except:
        pass

    return min_dis_stor, parent_node_stor, unvisited, end_check


def check_right(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited):
    end_check = False
    try:
        right_node = maze_array[selected_node[0], selected_node[1] + 1]
        if right_node != 1:
            new_dis = min_dis_stor[selected_node[0], selected_node[1]] + 1
            if new_dis < min_dis_stor[selected_node[0], selected_node[1] + 1]:
                min_dis_stor[selected_node[0], selected_node[1] + 1] = new_dis
                parent_node_stor[selected_node[0], selected_node[1] + 1] = 4
                unvisited.update({(selected_node[0], selected_node[1] + 1): new_dis})
            if right_node == 3:
                end_check = True
    except:
        pass

    return min_dis_stor, parent_node_stor, unvisited, end_check


def check_down(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited):
    end_check = False
    try:
        down_node = maze_array[selected_node[0] + 1, selected_node[1]]
        if down_node != 1:
            new_dis = min_dis_stor[selected_node[0], selected_node[1]] + 1
            if new_dis < min_dis_stor[selected_node[0] + 1, selected_node[1]]:
                min_dis_stor[selected_node[0] + 1, selected_node[1]] = new_dis
                parent_node_stor[selected_node[0] + 1, selected_node[1]] = 1
                unvisited.update({(selected_node[0] + 1, selected_node[1]): new_dis})
            if down_node == 3:
                end_check = True
    except:
        pass

    return min_dis_stor, parent_node_stor, unvisited, end_check


def check_left(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited):
    end_check = False
    try:
        left_node = maze_array[selected_node[0], selected_node[1] - 1]
        if left_node != 1:
            new_dis = min_dis_stor[selected_node[0], selected_node[1]] + 1
            if new_dis < min_dis_stor[selected_node[0], selected_node[1] - 1]:
                min_dis_stor[selected_node[0], selected_node[1] - 1] = new_dis
                parent_node_stor[selected_node[0], selected_node[1] - 1] = 2
                unvisited.update({(selected_node[0], selected_node[1] - 1): new_dis})
            if left_node == 3:
                end_check = True
    except:
        pass

    return min_dis_stor, parent_node_stor, unvisited, end_check


def dijkstras_main(maze_array):
    min_dis_stor, parent_node_stor, unvisited = initiate(maze_array)

    running = True
    impossible = False
    while running:
        try:
            selected_node = min(unvisited, key=unvisited.get)
            if unvisited[selected_node] == 9999:
                running = False
                impossible = True
                break
        except:
            running = False

        if maze_array[selected_node] != 2:
            pygame.draw.rect(config.dis, config.light_blue,
                             [(selected_node[1] * config.square_size) + config.square_size / 2,
                              (selected_node[0] * config.square_size) + config.square_size / 2, config.square_size / 2,
                              config.square_size / 2])
            pygame.display.update()
            time.sleep(0.05)
            pygame.draw.rect(config.dis, config.light_blue,
                             [selected_node[1] * config.square_size, selected_node[0] * config.square_size,
                              config.square_size, config.square_size])
            pygame.display.update()
            time.sleep(0.05)

        board_state_check = maze_array[selected_node[0], selected_node[1]]
        if board_state_check != 1:
            min_dis_stor, parent_node_stor, unvisited, end_check_up = check_up(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_right = check_right(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_down = check_down(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_left = check_left(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            if end_check_up or end_check_right or end_check_down or end_check_left:
                running = False
            else:
                del unvisited[(selected_node[0], selected_node[1])]

    return parent_node_stor, impossible
