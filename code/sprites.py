import pygame
from settings import *
from support import import_assets, import_folder
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
    def __init__(self, pos, surface, name, apple_image, add_item, groups):
        # self.hitbox = Vector2(self.rect.center)
        super().__init__(pos, surface, LAYERS['main'], groups)
        self.name = name
        self.apple_image = apple_image 
        self.add_item = add_item
        self.og_img = self.image



        self.offset = pygame.Vector2(self.rect.topleft)


        self.health = 3
        self.stump_path = f'PydewValley/graphics/stumps/{self.name.lower()}.png'
        self.stump_image = pygame.image.load(self.stump_path).convert_alpha()

        self.tree_life = True
        self.create_fruit()
        
    def damage(self):
        if self.tree_life:
            if len(self.apple_sprites.sprites()) > 0:
                random_apple = random.choice(self.apple_sprites.sprites())
                random_apple.kill()
                Particle(random_apple.rect.topleft, self.apple_image, LAYERS['fruit'], self.groups()[0])
                self.add_item('apple')
            

            else:
                print(f"OUCH! {self.health} {self.tree_life}")
                self.health -= 1
                Particle(self.rect.topleft, self.image, LAYERS['fruit'], self.groups()[0], 0.05)
                if self.health <= 0:
                    Particle(self.rect.topleft, self.image, LAYERS['fruit'], self.groups()[0])
                    
                    self.image = self.stump_image
                    self.rect = self.image.get_frect(midbottom=self.rect.midbottom)
                    self.hitbox = self.rect
                    self.tree_life = False
    
    def reset(self):
        self.tree_life = True
        self.image = self.og_img
        self.rect = self.image.get_frect(midbottom=self.rect.midbottom)
        self.health = 3
        for apple in self.apple_sprites.sprites():
            apple.kill()
        self.create_fruit() 

    def create_fruit(self):
        self.apple_sprites = pygame.sprite.Group()
        num_apples = random.randint(0, 3)
        apple_list = random.sample(APPLE_POS[self.name], num_apples)
        all_sprites = self.groups()[0]
        for appple_pos in apple_list:
            Generic(appple_pos+self.offset, self.apple_image, LAYERS['fruit'], [all_sprites, self.apple_sprites])


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


class Particle(Generic):
    def __init__(self, pos, surface, z, groups, duration = 0.2):
        super().__init__(pos, surface, z, groups)
        self.duration = duration

        mask_surface = pygame.mask.from_surface(surface)
        new_surface = mask_surface.to_surface()
        new_surface.set_colorkey("black")
        self.image = new_surface

    def update(self, dt):
        self.duration -= dt
        if self.duration <= 0:
            self.kill()

class FadingParticle(Particle):
    def __init__(self, pos, surface, z, groups, duration=0.2):
        super().__init__(pos, surface, z, groups)
        self.duration = duration

class Interaction(Generic):
    def __init__(self, pos, size, name, groups):
        surface = pygame.Surface(size)
        super().__init__(pos, surface, LAYERS['main'], groups)
        self.name = name

class Drops(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, LAYERS['rain floor'], groups)
        self.lifetime = random.random() * 0.1 + 0.4

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()


class FallingDrops(Drops):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
        self.pos = pos

        self.Falling = True
    

        self.z == LAYERS['rain drops']

        self.direction = pygame.Vector2(-2, 4)
        self.speed = random.randint(200, 250)
    
    def update(self, dt):
        super().update(dt)
        movement = self.direction * self.speed * dt
        self.pos += movement
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.Falling = False
            self.kill()

            # Drops((self.rect.x, self.rect.y), )
