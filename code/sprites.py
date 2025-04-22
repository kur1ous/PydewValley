import pygame
from settings import *
from support import import_assets


class Generic(pygame.sprite.Sprite):

    def __init__(self, pos, surface, z, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=pos)
        self.z = z

class Water(Generic):

    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 6
        self.rect = self.images

        super().__init__(pos, frames[0], LAYERS['main'], groups)


    @property
    def images(self):
        return self.frames[int(self.frame_index)]
    
    def animate(self, dt):
        self.frame_index += dt * self.animation_speed
        self.frame_index = self.frame_index % len(self.frames)
        print(int(self.frame_index))



    def update(self, dt):
        self.animate(dt)