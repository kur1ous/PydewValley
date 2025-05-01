import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from sprites import Generic
from support import import_folder, import_assets



class SoilTile(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, LAYERS['soil'], groups)


class SoilLayer:

    def __init__(self, all_sprites):
        self.soil_sprites = pygame.sprite.Group()


        ground = pygame.image.load("PydewValley/graphics/world/ground.png")
        width_tiles = ground.get_width() // TILE_SIZE
        height_tiles = ground.get_height() // TILE_SIZE

        self.all_sprites = all_sprites
        self.soil_image = pygame.image.load('PydewValley/graphics/soil/soil.png').convert_alpha()
        self.soil_images = import_assets("PydewValley/graphics/soil/")
        print(f'images: {self.soil_images}')





        self.grid = [ [[] for col in range(width_tiles)] for row in range(height_tiles) ]

        tmx_data = load_pygame("PydewValley/data/map.tmx")

        for x, y, img, in tmx_data.get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def to_tile_coordinates(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        return int(x), int(y)
    
    def use_hoe(self, pos):
        x, y = self.to_tile_coordinates(pos)
        if 'F' in self.grid[y][x]:
            SoilTile((x*TILE_SIZE, y*TILE_SIZE), self.soil_image, [self.all_sprites, self.soil_sprites])
            print("Farmable!")
        else:
            print("Not Farmable!")
            print(pos)