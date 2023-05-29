'''

This file contains dijkstras algorithm based on an array detailing the structure of the maze.

'''

import pygame
import time
import config
import solving_funcs


def dijkstras_main(maze_array):
    # main running loop for Dijkstras algorithm.
    min_dis_stor, parent_node_stor, unvisited = solving_funcs.initiate(maze_array)  # initiates the variables used throughout the algorithm.
    # see the comments under the initiate function for details of these.

    running = True
    impossible = False
    while running:
        try:
            selected_node = min(unvisited, key=unvisited.get)  # identifies node in queue with smallest calculated distance to end node at that stage.
            if unvisited[selected_node] == 9999:  # this happens when the algorithm finishes checking all nodes within the reachable area and attempts to check a node on the other side of the walls.
                running = False
                impossible = True  # indicater for the maze being impossible to solve.
                break
        except:
            running = False  # once the queue is empty, this triggers.

        if maze_array[selected_node] != 2:  # avoids overlaying the start node.
            solving_funcs.animate_node(selected_node)  # animates the current node.

        board_state_check = maze_array[selected_node[0], selected_node[1]]  # checks state of current node.
        if board_state_check != 1:  # ignores walls.
            min_dis_stor, parent_node_stor, unvisited, end_check_up = solving_funcs.check_up(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_right = solving_funcs.check_right(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_down = solving_funcs.check_down(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            min_dis_stor, parent_node_stor, unvisited, end_check_left = solving_funcs.check_left(maze_array, selected_node, min_dis_stor, parent_node_stor, unvisited)
            if end_check_up or end_check_right or end_check_down or end_check_left:  # checks if any of the adjacent nodes have been found to be the end node.
                running = False  # stops the algorithm when end node has been found.
            else:  
                del unvisited[(selected_node[0], selected_node[1])]  # deletes current node from queue.

    return parent_node_stor, impossible
