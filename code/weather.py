import pygame
from support import import_folder
from sprites import Drops, FallingDrops
import random

class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        
        self.rain_drops = import_folder("PydewValley/graphics/rain/drops/")
        self.rain_floor = import_folder("PydewValley/graphics/rain/floor/")

        ground = pygame.image.load("PydewValley/graphics/world/ground.png")
        self.width, self.height = ground.get_size()
    
    def update(self):
        self.FallingDrop = FallingDrops((random.randint(0, self.width), random.randint(0, self.height)), random.choice(self.rain_drops), self.all_sprites)

        # if self.FallingDrop.Falling == False: # look into fixing this
        Drops((self.FallingDrop.rect.x, self.FallingDrop.rect.y), random.choice(self.rain_floor), self.all_sprites)

        

