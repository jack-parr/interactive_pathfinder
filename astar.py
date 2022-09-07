"""

This file contains the A* algorithm based on an array of the maze.

"""

import numpy as np
import pygame
import time
import math
import config
import dijkstras as dijk


def heuristic(board):
    board_dims = np.shape(board)
    heuristic_stor = np.full(board_dims, 9999)
    coords_find = np.where(board == 3)
    end_coords = [coords_find[0][0], coords_find[1][0]]

    for row in range(0, board_dims[0]):
        for col in range(0, board_dims[1]):
            state_check = board[row, col]
            if state_check != 1:
                end_dis = math.sqrt(1.5 * ((row - end_coords[0])**2 + (col - end_coords[1])**2))
                heuristic_stor[row, col] = end_dis

    return heuristic_stor


def apply_heuristics(unvisited, heuristics):
    for coords in unvisited:
        if unvisited[coords] != 9999:
            unvisited[coords] += heuristics[coords]
            heuristics[coords] = 0
    return unvisited, heuristics


def astar_main(maze_array):
    heuristic_stor = heuristic(maze_array)
    min_dis_stor, parent_node_stor, unvisited = dijk.initiate(maze_array)
    start_coords = min(unvisited, key=unvisited.get)
    unvisited[start_coords] += heuristic_stor[start_coords]

    running = True
    impossible = False
    while running:
        try:
            unvisited, heuristic_stor = apply_heuristics(unvisited, heuristic_stor)
            selected_node = min(unvisited, key=unvisited.get)
            if unvisited[selected_node] == 9999:
                running = False
                impossible = True
                break
        except:
            running = False

        if maze_array[selected_node] != 2:
            pygame.draw.rect(config.dis, config.pink,
                             [(selected_node[1] * config.square_size) + config.square_size / 2,
                              (selected_node[0] * config.square_size) + config.square_size / 2, config.square_size / 2,
                              config.square_size / 2])
            pygame.display.update()
            time.sleep(0.05)
            pygame.draw.rect(config.dis, config.pink,
                             [selected_node[1] * config.square_size, selected_node[0] * config.square_size,
                              config.square_size, config.square_size])
            pygame.display.update()
            time.sleep(0.05)

        board_state_check = maze_array[selected_node[0], selected_node[1]]
        if board_state_check != 1:
            min_dis_stor, parent_node_stor, unvisited, end_check_up = dijk.check_up(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_right = dijk.check_right(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_down = dijk.check_down(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_left = dijk.check_left(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            if end_check_up or end_check_right or end_check_down or end_check_left:
                running = False
            else:
                del unvisited[(selected_node[0], selected_node[1])]

    return parent_node_stor, impossible
