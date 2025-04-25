import pygame
from settings import *
from support import import_assets
import random

class Generic(pygame.sprite.Sprite):

    def __init__(self, pos, surface, z, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)

        self.hitbox = self.rect.inflate(-0.2* self.rect.width, -0.75* self.rect.height)
        self.z = z


class Wildflower(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, LAYERS['main'], groups)

class Tree(Generic):
    def __init__(self, pos, surface, name, apple_image, groups):
        # self.hitbox = Vector2(self.rect.center)
        super().__init__(pos, surface, LAYERS['main'], groups)
        self.name = name
        self.apple_image = apple_image 

        self.apple_sprites = pygame.sprite.Group()
        num_apples = random.randint(0, 3)
        apple_list = random.sample(APPLE_POS[self.name], num_apples)
        all_sprites = self.groups()[0]

        self.offset = pygame.Vector2(self.rect.topleft)

        self.health = 3
        self.stump_path = f'PydewValley/graphics/stumps/{self.name.lower()}.png'
        self.stump_image = pygame.image.load(self.stump_path).convert_alpha()

        self.tree_life = True

        for appple_pos in apple_list:
            Generic(appple_pos+self.offset, self.apple_image, LAYERS['fruit'], [all_sprites, self.apple_sprites])
    def damage(self):
        if self.tree_life:
            if len(self.apple_sprites.sprites()) > 0:
                random_apple = random.choice(self.apple_sprites.sprites())
                random_apple.kill()
            else:
                print(f"OUCH! {self.health}")
                self.health -= 1
                if self.health <= 0:
                    self.image = self.stump_image
                    self.tree_life = False
            


class Water(Generic):

    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 6


        super().__init__(pos, frames[0], LAYERS['water'], groups)



    
    def animate(self, dt):
        self.frame_index += dt * self.animation_speed
        self.frame_index %= len(self.frames)
        self.image = self.frames[int(self.frame_index)]



    def update(self, dt):
        self.animate(dt)