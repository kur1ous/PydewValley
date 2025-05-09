import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from sprites import Generic
from support import import_folder, import_assets, import_folder_dict
import random



class SoilTile(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, LAYERS['soil'], groups)

class WaterTile(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, LAYERS['soil water'], groups)

class Plant(Generic):
    def __init__(self, pos, images, plant_type, check_watered, age, max_age, growth_speed, groups):
        self.images = images
        super().__init__(pos, self.images[0], LAYERS['ground plant'], groups)
        self.plant_type = plant_type
        self.check_watered = check_watered

        self.rect.midbottom = pos

        self.age = age
        self.max_age = max_age
        self.growth_speed = growth_speed

    def grow(self):
        if self.check_watered:
            self.age += self.growth_speed
            print(self.age)
            if self.age >= self.max_age: 
                self.age = self.max_age
            self.image = self.images[self.age]
        else: return

                
    

            


class SoilLayer:

    def __init__(self, all_sprites):
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        #rain toggle
        self.raining = False

        ground = pygame.image.load("PydewValley/graphics/world/ground.png")
        width_tiles = ground.get_width() // TILE_SIZE
        height_tiles = ground.get_height() // TILE_SIZE

        self.all_sprites = all_sprites
        self.soil_image = pygame.image.load('PydewValley/graphics/soil/soil.png').convert_alpha()
        self.soil_images = import_folder_dict("PydewValley/graphics/soil/")

        self.water_images = import_folder("PydewValley/graphics/soil_water")

        self.plant_images = import_assets("PydewValley/graphics/fruit")

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
                self.grid[y-1][x].append('top')
                self.grid[y+1][x].append('bottom')
            else: print("Already has Soil!")
            
            self.create_soil_sprites()
            if self.raining:
                self.water(pos)
                
            # SoilTile((x*TILE_SIZE, y*TILE_SIZE), self.soil_image, [self.all_sprites, self.soil_sprites])
            print("Farmable!")
            
        else:
            print("Not Farmable!")
            print(pos)

    def create_soil_sprites(self):
        for soil_sprite in self.soil_sprites:
            soil_sprite.kill()

        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if 'X' in col:
                    left = 'left' in col
                    right = 'right' in col
                    bottom = 'bottom' in col
                    top = 'top' in col

                    file_name = ""

                    if not any([left, top, right, bottom]):
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
                    print(file_name)
    
    def water(self, pos):
        x, y = self.to_tile_coordinates(pos)
        if 'X' in self.grid[y][x]:
            if 'W' not in self.grid[y][x]:
                self.grid[y][x].append('W')

                img = self.water_images[random.randint(0, len(self.water_images) - 1)]
                WaterTile((x * TILE_SIZE, y * TILE_SIZE), img, [self.all_sprites, self.water_sprites])
                print(f'Added W at {pos}')
            else: print("Already Watered!")
        else: print(f"No Soil to Water at {pos}!")
    
    def remove_water(self):
        self.raining = False
        for water_sprite in self.water_sprites:
            water_sprite.kill()
        for row in self.grid:
            for cell in row:
                while 'W' in cell:
                    cell.remove('W')
                    print(f'wter removed at {cell}')
        
    
    def water_all(self):
        self.raining = True
        for soil in self.soil_sprites:
            self.water(soil.rect.center)

    def plant_seed(self, pos, seed_type):
        x, y = self.to_tile_coordinates(pos)
        if 'X' in self.grid[y][x] and 'P' not in self.grid[y][x]:
            self.grid[y][x].append('P')
            print(f"planting {seed_type}")
            plant_x = (x + 0.5) * TILE_SIZE
            plant_y = (y+1) * TILE_SIZE

            plant_y -= 16 if seed_type == "corn" else 8
            Plant((plant_x, plant_y), self.plant_images[seed_type], seed_type, self.check_watered((x*TILE_SIZE, y*TILE_SIZE)), 0, 3, GROW_SPEED[seed_type], [self.all_sprites, self.plant_sprites])

    def check_watered(self, pos): # fix this method
        x, y = self.to_tile_coordinates(pos)
        if 'W' in self.grid[y][x] and 'P' in self.grid[y][x]: 
                return True
        return False

    def grow_plnats(self):
        for plant in self.plant_sprites:
            plant.grow()

                
        
        



        






