import pygame
from settings import *
from support import import_assets
from mytimer import Timer
from debug import get_coords

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, up_key, down_key, left_key, right_key, run_key, use_key, plant_key, tool_scroll_key, seed_scroll_key, collision_sprites, tree_sprites, interaction_sprite, next_day, soil_layer, open_menu, groups):
        super().__init__(groups)

        self.animations = import_assets("PydewValley/graphics/character/")
        self.status = "right"
        self.frame_index = 0
        self.collision_sprites = collision_sprites
        self.tree_sprites = tree_sprites
        self.interaction_sprites = interaction_sprite
        self.soil_layer = soil_layer
        self.open_menu = open_menu



        self.next_day = next_day
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
        
        self.input_locked = False

        self.z = LAYERS['main']

        self.run_mult = 1

        self.animation_speed = 5

        self.is_tool_active = False

        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.inflate(-126,-70)

    
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
            'tool use': Timer(0.5, self.use_tool),
            'seed use': Timer(1, self.use_seed),
        }

        self.item_inventory = {
            'wood' : 0,
            'apple' : 0,
            'corn' : 0,
            'tomato' : 0
        }

        self.seed_inventory = {
            'corn': 5,
            'tomato': 5
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
    
    @property
    def locked(self):
        return self.timers['seed use'].active or self.timers['tool use'].active or self.input_locked
    
    def use_seed(self):
        interaction_point = self.get_interaction_point()
        if self.seed_inventory[self.selected_seed] > 0 and self.soil_layer.check_if_seedable(interaction_point):
            self.soil_layer.plant_seed(interaction_point, self.selected_seed)
            self.seed_inventory[self.selected_seed] -= 1


    
    def use_tool(self):
        print(f'Using {self.selected_tool}')
        interaction_point = self.get_interaction_point()
        if self.selected_tool == 'axe':
            for tree in self.tree_sprites:
                if tree.rect.collidepoint(interaction_point):
                    print(f"chopping {tree}")
                    tree.damage()
        if self.selected_tool == 'hoe':
                self.soil_layer.use_hoe(interaction_point)
        if self.selected_tool == "water":
            self.soil_layer.water(interaction_point)

    def check_interation(self):
        for sprite in self.interaction_sprites:
            if sprite.name == 'Bed':
                if sprite.rect.collidepoint(self.rect.center):
                    print(f'{sprite.name}, Day reset!')
                    self.next_day()
            elif sprite.name == "Trader":
                if sprite.rect.collidepoint(self.rect.center):
                    self.open_menu()

            else:
                print(sprite.name)

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
        if self.locked: return
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
        
        if keys_just_pressed[pygame.K_1]:
            get_coords(self)

        if keys_just_pressed[pygame.K_RETURN]:
            self.check_interation()
        
        if keys[self.use_key]:
            self.timers['tool use'].activate()
    
        elif keys[self.plant_key]:
            self.timers['seed use'].activate()

    def add_item(self, item_name):
        self.item_inventory[item_name] += 1
        print(self.item_inventory)
    
    def movement(self, dt):
        if self.locked: return
        if self.direction.magnitude() != 0:
            self.direction.normalize_ip()
        self.hitbox.x += self.direction.x * self.speed * dt
        
        for sprite in self.collision_sprites:
            if self.hitbox.colliderect(sprite.hitbox):
                if self.direction.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                if self.direction.x < 0:
                    self.hitbox.left = sprite.hitbox.right
                

        self.hitbox.y += self.direction.y * self.speed * dt 
        for sprite in self.collision_sprites:
            if self.hitbox.colliderect(sprite.hitbox):
                if self.direction.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                if self.direction.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom

        self.rect.center = self.hitbox.center

    def update_timers(self, dt):
        for timer in self.timers.values():
            timer.update(dt)
    
    def get_interaction_point(self):
        direction = self.status.split("_")[0]
        offset = pygame.Vector2(PLAYER_TOOL_OFFSET[direction])
        return self.rect.center + offset
    
    def lock_input(self):
        self.input_locked = True

    def unlock_input(self):
        self.input_locked = False




    def update(self, dt):
        self.speed = self.base_speed * self.run_mult
        self.input()
        self.get_status()
        self.update_timers(dt)
        self.animate(dt)
        self.movement(dt)
    

