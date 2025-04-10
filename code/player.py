import pygame
from settings import *
from support import import_assets

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, up_key, down_key, left_key, right_key, run_key, groups):
        super().__init__(groups)

        self.animation = import_assets("PydewValley/graphics/character/")

        self.up_key = up_key
        self.down_key = down_key
        self.right_key = right_key
        self.left_key = left_key
        self.run_key = run_key
        self.run_mult = 1

        self.image = self.animation['left_axe'][0]

        self.rect = self.image.get_frect(center=pos)
        
        self.direction = pygame.Vector2()
        self.base_speed = 200
    
    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.y = keys[self.down_key] - keys[self.up_key] #true/false -- 1/0
        self.direction.x = keys[self.right_key] - keys[self.left_key]
        if keys[self.run_key]:
            self.run_mult = 1.2
        else:
            self.run_mult = 1
    
    def movement(self, dt):
        if self.direction.magnitude() != 0:
            self.direction.normalize_ip()
        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        self.speed = self.base_speed * self.run_mult
        self.input()
        self.movement(dt)

