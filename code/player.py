import pygame
from settings import *
from support import import_assets
from mytimer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, up_key, down_key, left_key, right_key, run_key, use_key, groups):
        super().__init__(groups)

        self.animations = import_assets("PydewValley/graphics/character/")
        self.status = "right"
        self.frame_index = 0
        # self.image = self.animations['up'][0]


        self.up_key = up_key
        self.down_key = down_key
        self.right_key = right_key
        self.left_key = left_key
        self.run_key = run_key
        self.use_key = use_key
        self.run_mult = 1

        self.animation_speed = 5

        self.is_tool_active = False

        self.rect = self.image.get_frect(center=pos)
    
        self.direction = pygame.Vector2()
        self.base_speed = 200

        self.timers = {
            'tool use': Timer(0.35)
        }
        self.selected_tool = 'axe'

    @property
    def image(self):
        return self.animations[self.status][int(self.frame_index)]

    def animate(self, dt):

        self.frame_index += dt * self.animation_speed * self.run_mult
        self.frame_index = self.frame_index % len(self.animations[self.status])
        # self.image = self.animations[self.status][int(self.frame_index)]

    def get_status(self):
 
        self.status = self.status.split("_")[0]
  
        if self.direction.y > 0:
            self.status = 'down'
        elif self.direction.y < 0:
            self.status = 'up'
        elif self.direction.x > 0:
            self.status = 'right'
        elif self.direction.x < 0:
            self.status = 'left'

        if self.direction.magnitude() == 0:
            self.status += '_idle'

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.y = keys[self.down_key] - keys[self.up_key] #true/false -- 1/0
        self.direction.x = keys[self.right_key] - keys[self.left_key]

        if keys[self.run_key]:
            self.run_mult = 2
        else:
            self.run_mult = 1

        if keys[self.use_key]:
            self.timers['tool use'].activate()
    
    def movement(self, dt):
        if self.direction.magnitude() != 0:
            self.direction.normalize_ip()
        self.rect.center += self.direction * self.speed * dt

    def update_timers(self, dt):
        for timer in self.timers.values():
            timer.update(dt)

    def update(self, dt):
        self.speed = self.base_speed * self.run_mult
        self.input()
        self.get_status()
        self.update_timers()
        self.animate(dt)
        self.movement(dt)
    

