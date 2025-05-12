import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, surface, offset, soil_grid):
        # print(offset)
        offset = pygame.Vector2(offset)
        offset -= pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.soil_grid = soil_grid

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    hitbox = sprite.hitbox.copy()
                    hitbox.topleft -= offset
                    surface.blit(sprite.image, sprite.rect.topleft - offset)
                    # pygame.draw.rect(surface, "red", hitbox, 2)
        		
    
        if soil_grid:
            for row_idx, row in enumerate(self.soil_grid):
                for col_idx, cell in enumerate(row):
                    tile_x = col_idx * TILE_SIZE
                    tile_y = row_idx * TILE_SIZE
                    rect = pygame.Rect(tile_x, tile_y, TILE_SIZE, TILE_SIZE)
                    rect.topleft -= offset

                    color = 'green' if 'F' in cell else 'red'
                    color2 = 'blue' if 'P' in cell else 'white'
                    # pygame.draw.rect(surface, color2, rect, 1)

			