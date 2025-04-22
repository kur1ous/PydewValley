from settings import *
import pygame

def get_coords(player):
    keys_just_pressed = pygame.key.get_just_pressed()
    if keys_just_pressed[pygame.K_1]:
        print(player.rect)

