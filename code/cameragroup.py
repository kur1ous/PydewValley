import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, surface, offset):
        offset = pygame.Vector2(offset)
        offset -= pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    surface.blit(sprite.image, sprite.rect.topleft - offset)
