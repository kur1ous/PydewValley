from settings import *
import pygame

def get_coords(player):
    print(player.rect)

def click_coords():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)