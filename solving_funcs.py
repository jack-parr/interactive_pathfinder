'''

This file contains fundamental functions used by the solving algorithms.

'''

import numpy as np
import pygame
import time
import config


def initiate(maze):
    # creates the working and storage variables used throughout the algorithm. 
    # In the 'maze' variable: 0 = empty, 1 = wall, 2 = start, 3 = end. Array is arranged as a grid mapping the nodes on the display window.
    # The maze is laid out in the 'maze' variable as [row, col], so you have to think about it like (y, x).
    board_dims = np.shape(maze)  # dimensions of the board.
    min_dis_stor = np.full(board_dims, 9999)  # stores the minimum distance from the start node to each node.
    parent_node_stor = np.zeros(board_dims, int)  # stores the parent nodes of the solved path.
    unvisited = {}  # queue of unvisited nodes.
    for row in range(0, board_dims[0]):
        for col in range(0, board_dims[1]):
            state_check = maze[row, col]  # isolates state of each node.
            if state_check != 1:
                unvisited.update({(row, col): 9999})  # does not add wall nodes to the dictionary.
                if state_check == 2:
                    unvisited.update({(row, col): 0})  # marks the start node in the dictionary so that the algorithm starts there.
                    min_dis_stor[row, col] = 0  # marks min_dis_stor with a 0 for the start node.

    return min_dis_stor, parent_node_stor, unvisited


def check_up(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited):
    # checks the node above the selected node, which is provide as [row, col].
    end_check = False
    try:
        up_node = maze_array[selected_node[0] - 1, selected_node[1]]  # isolates state of node above.
        if up_node != 1:  # ignores if it is a wall.
            new_dis = min_dis_stor[selected_node[0], selected_node[1]] + 1  # calculates distance of path from selected node to the node above.
            if new_dis < min_dis_stor[selected_node[0] - 1, selected_node[1]]:  # checks if calculated distance is lower than current best path to that node.
                min_dis_stor[selected_node[0] - 1, selected_node[1]] = new_dis  # adds new best distance to min_dis_stor.
                parent_node_stor[selected_node[0] - 1, selected_node[1]] = 3  # updates parent_node_stor with direction of path.
                unvisited.update({(selected_node[0] - 1, selected_node[1]): new_dis})  # updates queue with new distance value.
            if up_node == 3:
                end_check = True  # indicates that the end node has been found.
    except:
        pass  # passes if check fails.

    return min_dis_stor, parent_node_stor, unvisited, end_check


def animate_node(selected_node):
    pygame.draw.rect(config.dis, config.light_blue,
                             [(selected_node[1] * config.square_size) + config.square_size / 2,
                              (selected_node[0] * config.square_size) + config.square_size / 2, config.square_size / 2,
                              config.square_size / 2])  # draws small square within current node.
    pygame.display.update()
    time.sleep(0.05)  # delay so the solving animation is visible.
    pygame.draw.rect(config.dis, config.light_blue,
                        [selected_node[1] * config.square_size, selected_node[0] * config.square_size,
                        config.square_size, config.square_size])  # draws full square within current node.
    pygame.display.update()
    time.sleep(0.05)  # delay so the solving animation is visible.


def check_right(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited):
    # checks the node to the right of the selected node, which is provided as [row, col].
    end_check = False
    try:
        right_node = maze_array[selected_node[0], selected_node[1] + 1]  # isolates the state of node to the right.
        if right_node != 1:  # ignores if it is a wall.
            new_dis = min_dis_stor[selected_node[0], selected_node[1]] + 1  # calculates distance of path from selected node to the node to the right.
            if new_dis < min_dis_stor[selected_node[0], selected_node[1] + 1]:  # checks if calculated distance is lower than current best path to that node.
                min_dis_stor[selected_node[0], selected_node[1] + 1] = new_dis  # adds new best distance to min_dis_stor.
                parent_node_stor[selected_node[0], selected_node[1] + 1] = 4  # updates parent_node_stor with direction of path.
                unvisited.update({(selected_node[0], selected_node[1] + 1): new_dis})  # updates queue with new distance value.
            if right_node == 3:
                end_check = True  # indicates that the end node has been found.
    except:
        pass  # passes if check fails.

    return min_dis_stor, parent_node_stor, unvisited, end_check


def check_down(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited):
    # checks the node below the selected node, which is provided as [row, col].
    end_check = False
    try:
        down_node = maze_array[selected_node[0] + 1, selected_node[1]]  # isolates the state of node below.
        if down_node != 1:  # ignores if it is a wall.
            new_dis = min_dis_stor[selected_node[0], selected_node[1]] + 1  # calculates distance of path from selected node to the node below.
            if new_dis < min_dis_stor[selected_node[0] + 1, selected_node[1]]:  # checks if calculated distance is lower than current best path to node below.
                min_dis_stor[selected_node[0] + 1, selected_node[1]] = new_dis  # adds new best distance to min_dis_stor.
                parent_node_stor[selected_node[0] + 1, selected_node[1]] = 1  # updates parent_node_stor with direction of path.
                unvisited.update({(selected_node[0] + 1, selected_node[1]): new_dis})  # updates queue with new distance value.
            if down_node == 3:
                end_check = True  # indicates that the end node has been found.
    except:
        pass  # passes if check fails.

    return min_dis_stor, parent_node_stor, unvisited, end_check


def check_left(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited):
    # checks the node to the left of the selected node, which is provided as [row, col].
    end_check = False
    try:
        left_node = maze_array[selected_node[0], selected_node[1] - 1]  # isolates the state of the node to the left.
        if left_node != 1:  # ignores if it is a wall.
            new_dis = min_dis_stor[selected_node[0], selected_node[1]] + 1  # calculates distance of path from selected node to the node to the left.
            if new_dis < min_dis_stor[selected_node[0], selected_node[1] - 1]:  # checks if calculated distance is lower than current best path to node.
                min_dis_stor[selected_node[0], selected_node[1] - 1] = new_dis  # adds new best distance to min_dis_stor.
                parent_node_stor[selected_node[0], selected_node[1] - 1] = 2  # updates parent_node_stor with direction of path.
                unvisited.update({(selected_node[0], selected_node[1] - 1): new_dis})  # updates queue with new distance value.
            if left_node == 3:
                end_check = True  # indicates that the end node has been found.
    except:
        pass  # passes if check fails.

    return min_dis_stor, parent_node_stor, unvisited, end_check
