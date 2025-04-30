import pygame
from settings import *
from pytmx.util_pygame import load_pygame

class SoilLayer:

    def __init__(self):
        self.soil_sprites = pygame.sprite.Group()

        ground = pygame.image.load("PydewValley/graphics/world/ground.png")
        width_tiles = ground.get_width() // TILE_SIZE
        height_tiles = ground.get_height() // TILE_SIZE




        self.grid = [ [[] for col in range(width_tiles)] for row in range(height_tiles) ]

        tmx_data = load_pygame("PydewValley/data/map.tmx")

        for x, y, img, in tmx_data.get_layer_by_name('Farmable').tiles():
            self.grid[x][y].append('F')

    def to_tile_coordinates(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        return int(x), int(y)
    
    def use_hoe(self, pos):
        x, y = self.to_tile_coordinates((1000, 400))
        if 'F' in self.grid[y][x]:
            print("Farmable!")
        else:
            print("Not Farmable!")
            print(pos)