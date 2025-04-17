import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, surface, offset):
        offset = pygame.Vector2(offset)
        offset -= pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        for sprite in self.sprites():
            surface.blit(sprite.image, sprite.rect.topleft - offset)
