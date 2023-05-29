'''

This file contains configuration variables for the display window.

'''

import pygame

white = (255, 255, 255)  # RGB colour system.
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (0, 255, 255)
orange = (255, 165, 0)
pink = (255, 192, 203)
mode_colours = [white, black]

# DIMENSIONS
dis_width, dis_height = 400, 300
square_size = 20
banner_height = 80
canvas_height = dis_height - banner_height

# INITIALISING DISPLAY WINDOW
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.init()

mode_strings = ["Erase", "Draw"]
title_font = pygame.font.SysFont('verdana', 20, bold=True)
info_font = pygame.font.SysFont('verdana', 15)

# ADDING TEXTS
def add_texts():
    
    mode_text = info_font.render("Mode: " + str(mode_strings[1]), True, red)
    dis.blit(mode_text, [dis_width - 100, canvas_height])

    title_text = title_font.render("Maze Maker", True, black)
    dis.blit(title_text, [5, canvas_height])

    desc_text_1 = info_font.render("Draw a maze, press M to switch modes, R to reset.", True, black)
    desc_text_2 = info_font.render("Press D to run Dijkstras algorithm!", True, black)
    desc_text_3 = info_font.render("Press A to run the A* algorithm!", True, black)
    dis.blit(desc_text_1, [5, canvas_height + 20])
    dis.blit(desc_text_2, [5, canvas_height + 40])
    dis.blit(desc_text_3, [5, canvas_height + 60])


def impossible_text():
    dis.fill(white, (0, dis_height - banner_height, dis_width, banner_height))
    imp_text = info_font.render("This maze cannot be solved!", True, black)
    dis.blit(imp_text, [5, canvas_height + 10])
    res_text = info_font.render("Press R to Reset.", True, black)
    dis.blit(res_text, [5, canvas_height + 30])


def solved_text():
    dis.fill(white, (0, dis_height - banner_height, dis_width, banner_height))
    imp_text = info_font.render("The maze has been solved!", True, black)
    dis.blit(imp_text, [5, canvas_height + 10])
    res_text = info_font.render("Press R to Reset.", True, black)
    dis.blit(res_text, [5, canvas_height + 30])
