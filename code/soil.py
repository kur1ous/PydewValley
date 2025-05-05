import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from sprites import Generic
from support import import_folder, import_assets, import_folder_dict



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
        self.soil_images = import_folder_dict("PydewValley/graphics/soil/")

        print(f'image: {self.soil_images}')

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
            if 'X' not in self.grid[y][x]:
                self.grid[y][x].append('X')
                # left/right
                self.grid[y][x-1].append('left')
                self.grid[y][x+1].append('right')
                # up/down
                self.grid[y+1][x].append('up')
                self.grid[y-1][x].append('down')
            
            self.create_soil_sprites()
                
            # SoilTile((x*TILE_SIZE, y*TILE_SIZE), self.soil_image, [self.all_sprites, self.soil_sprites])
            print("Farmable!")
        else:
            print("Not Farmable!")
            print(pos)

    def create_soil_sprites(self):
        self.soil_sprites.empty()

        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if 'X' in col:
                    left = 'left' in col
                    right = 'right' in col
                    bottom = 'down' in col
                    top = 'up' in col

                    file_name = ""

                    if not all([left, top, right, bottom]):
                        file_name = "o" # no neighbours

                    elif all([left, top, right, bottom]):
                        file_name = "x"

                    else:
                        file_name += "l" if left else ""
                        file_name += "r" if right else ""
                        file_name += "b" if bottom else ""
                        file_name += "t" if top else ""
                    
                    img = self.soil_images[file_name]

                    SoilTile((x * TILE_SIZE, y * TILE_SIZE), img, [self.all_sprites, self.soil_sprites])