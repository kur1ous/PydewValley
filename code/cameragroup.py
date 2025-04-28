import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, surface, offset):
        # print(offset)
        offset = pygame.Vector2(offset)
        offset -= pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    hitbox = sprite.hitbox.copy()
                    hitbox.topleft -= offset
                    surface.blit(sprite.image, sprite.rect.topleft - offset)
                    # pygame.draw.rect(surface, "red", hitbox, 2)