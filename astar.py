'''

This file contains the A* algorithm based on an array detailing the structure of the maze.

'''

import numpy as np
import math
import solving_funcs


def heuristic(board):
    # initialises the heuristic variables.
    board_dims = np.shape(board)
    heuristic_stor = np.full(board_dims, 9999)  # makes a variable with the same dimensions as the board.
    coords_find = np.where(board == 3)  # finds coords of end node, in form [row, col].
    end_coords = [coords_find[0][0], coords_find[1][0]]  # formats the end node coords.

    for row in range(0, board_dims[0]):
        for col in range(0, board_dims[1]):  # iterates over every node of board.
            state_check = board[row, col]  # isolates the state of that node.
            if state_check != 1:  # ignores walls.
                end_dis = math.sqrt(1.5 * ((row - end_coords[0])**2 + (col - end_coords[1])**2))  # calculates straight line distance to end node, with a 1.5x adjuster.
                heuristic_stor[row, col] = end_dis  # puts calculated distance to end node in relevant position in heuristic_stor array.

    return heuristic_stor


def apply_heuristics(unvisited, heuristics):
    # applies the heuristics array to the unvisited queue.
    for coords in unvisited:  # 
        if unvisited[coords] != 9999:  # ignores if irrelevant node.
            unvisited[coords] += heuristics[coords]  # adds heuristic value to queue value.
            heuristics[coords] = 0  # removes heuristic value so that it doesn't get applied multiple times.

    return unvisited, heuristics


def astar_main(maze_array):
    # main running loop for A* algorithm.
    heuristic_stor = heuristic(maze_array)  # initiates heuristic values array.
    min_dis_stor, parent_node_stor, unvisited = solving_funcs.initiate(maze_array)  # initiates the variables used throughout the algorithm.
    start_coords = min(unvisited, key=unvisited.get)  # extracts start coords.
    unvisited[start_coords] += heuristic_stor[start_coords]  # applies heuristic to start coords in queue.

    running = True
    impossible = False
    while running:
        try:
            unvisited, heuristic_stor = apply_heuristics(unvisited, heuristic_stor)  # applies heuristics to any newly relevant nodes.
            selected_node = min(unvisited, key=unvisited.get)  # identifies node in queue with smallest calculated distance and heuristic sum to end node at that stage.
            if unvisited[selected_node] == 9999:  # this happens when the algorithm finishes checking all nodes within the reachable area and attempts to check a node on the other side of the walls.
                running = False
                impossible = True  # indicator that the maze is impossible to solve.
                break
        except:
            running = False  # once the queue is empty, this triggers.

        if maze_array[selected_node] != 2:  # avoids overlaying start node.
            solving_funcs.animate_node(selected_node)  # animates current node.

        board_state_check = maze_array[selected_node[0], selected_node[1]]  # extract state of current node.
        if board_state_check != 1:  # ignores walls.
            min_dis_stor, parent_node_stor, unvisited, end_check_up = solving_funcs.check_up(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_right = solving_funcs.check_right(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_down = solving_funcs.check_down(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_left = solving_funcs.check_left(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            if end_check_up or end_check_right or end_check_down or end_check_left:  # checks if any of the adjacent nodes are the end node.
                running = False  # stops the algorithm when the end node is found.
            else:
                del unvisited[(selected_node[0], selected_node[1])]  # deletes current node from queue.

    return parent_node_stor, impossible
