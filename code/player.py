import pygame
from settings import *
from support import import_assets
from mytimer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, up_key, down_key, left_key, right_key, run_key, use_key, plant_key, tool_scroll_key, seed_scroll_key, groups):
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
        self.plant_key = plant_key
        self.tool_scroll_key = tool_scroll_key
        self.seed_scroll_key = seed_scroll_key

        self.run_mult = 1

        self.animation_speed = 5

        self.is_tool_active = False

        self.rect = self.image.get_frect(center=pos)
    
        self.direction = pygame.Vector2()
        self.base_speed = 200

        self.tool_list = [
            'axe',
            'water',
            'hoe',
        ]
        self.tool_index = 0

        self.seed_list = [
            'corn',
            'tomato',
        ]
        self.seed_index = 0

        self.timers = {
            'tool use': Timer(2, self.use_tool),
            'seed use': Timer(1, self.use_seed),
        }


    @property
    def image(self):
        return self.animations[self.status][int(self.frame_index)]
    
    @property
    def selected_tool(self):
        return self.tool_list[self.tool_index]
    
    @property
    def selected_seed(self):
        return self.seed_list[self.seed_index]
    
    def use_seed(self):
        print(f'Planting {self.selected_seed}')
    
    def use_tool(self):
        print(f'Using {self.selected_tool}')

    def tool_scroll(self):
        self.tool_index += 1
        self.tool_index = self.tool_index % len(self.tool_list)
        print(self.tool_list[self.tool_index])

    def seed_scroll(self):
        self.seed_index += 1
        self.seed_index = self.seed_index % len(self.seed_list)
        print(self.seed_list[self.seed_index])

    def animate(self, dt):

        self.frame_index += dt * self.animation_speed
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

        if self.timers['tool use'].active:
            self.status += f'_{self.tool_list[self.tool_index]}'
        
        elif self.timers['seed use'].active:
            self.status += '_idle'

        elif self.direction.magnitude() == 0:
            self.status += '_idle'

    def input(self):
        keys = pygame.key.get_pressed()
        keys_just_pressed = pygame.key.get_just_pressed()

        self.direction.y = keys[self.down_key] - keys[self.up_key] #true/false -- 1/0
        self.direction.x = keys[self.right_key] - keys[self.left_key]

        if keys[self.run_key]:
            self.run_mult = 2
        else:
            self.run_mult = 1

        if keys_just_pressed[self.tool_scroll_key]:
            self.tool_scroll()
        
        if keys_just_pressed[self.seed_scroll_key]:
            self.seed_scroll()
        
        if keys[self.use_key]:
            self.timers['tool use'].activate()
    
        elif keys[self.plant_key]:
            self.timers['seed use'].activate()
    
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
        self.update_timers(dt)
        self.animate(dt)
        self.movement(dt)
    

