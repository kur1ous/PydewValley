import pygame
from settings import *
from support import import_assets


class Generic(pygame.sprite.Sprite):

    def __init__(self, pos, surface, z, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=pos)
        self.z = z

class Wildflower(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, LAYERS['main'], groups)

class Tree(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, LAYERS['main'], groups)


class Water(Generic):

    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 6


        super().__init__(pos, frames[0], LAYERS['water'], groups)



    
    def animate(self, dt):
        self.frame_index += dt * self.animation_speed
        self.frame_index %= len(self.frames)
        self.image = self.frames[int(self.frame_index)]



    def update(self, dt):
        self.animate(dt)