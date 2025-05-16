import pygame
from settings import *
from mytimer import Timer

class Overlay:
    def __init__(self, player):
        self.player = player

        self.menu_open = False

        self.tool_images = {tool_name: pygame.image.load(f'PydewValley/graphics/overlay/{tool_name}.png').convert_alpha() for tool_name in self.player.tool_list}
        print(self.tool_images)
        self.seed_images = {seed_name: pygame.image.load(f'PydewValley/graphics/overlay/{seed_name}.png').convert_alpha() for seed_name in self.player.seed_list}

        self.menu_items = {
            "buy": [list(self.player.seed_inventory.keys())],
            "sell": [list(self.player.item_inventory.keys())],
        }

        self.main_rect = pygame.FRect(0,0,400,100)
        self.main_rect.midtop = (SCREEN_WIDTH / 2, 100)

        self.font = pygame.font.Font("PydewValley/font/LycheeSoda.ttf", 30)
        self.buy_tab = self.font.render("Buy", False, "black")
        self.sell_tab = self.font.render("Sell", False, "black")
        self.buy_rect = self.buy_tab.get_frect(bottomleft = self.main_rect.topleft)
        self.sell_rect = self.sell_tab.get_frect(bottomleft = self.main_rect.bottomright)

    def open_menu(self):
        print("Opened!")
        self.menu_open = True
        self.player.lock_input()
    
    def input(self):
        keys_just_pressed = pygame.key.get_just_pressed()
        
        if keys_just_pressed[pygame.K_ESCAPE] and self.menu_open:
            self.menu_open = not self.menu_open
            self.player.unlock_input()
            print("Closed!")


    def draw(self, surface):
        img = self.tool_images[self.player.selected_tool]
        seedimg = self.seed_images[self.player.selected_seed]
        rect = img.get_frect(midbottom = OVERLAY_POSITIONS['tool'])
        seedrect = img.get_frect(midbottom = OVERLAY_POSITIONS['seed'])
        surface.blit(img, rect)
        surface.blit(seedimg, seedrect)

        if self.menu_open:
            surface.blit(self.buy_tab, self.buy_rect)
            surface.blit(self.sell_tab, self.sell_rect)
            pygame.draw.rect(surface, "black", self.main_rect)
    
    def update(self):
        self.input()
        