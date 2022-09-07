import pygame

white = (255, 255, 255)  # RGB colour system.
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (0, 255, 255)
orange = (255, 165, 0)
pink = (255, 192, 203)
colours = [white, black]

dis_width, dis_height = 400, 300  # setting up game window.
square_size, banner_height = 20, 80
canvas_height = dis_height - banner_height

dis = pygame.display.set_mode((dis_width, dis_height))
