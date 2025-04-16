import pygame
from settings import *
from mytimer import Timer

class Overlay:
    def __init__(self, player):
        self.player = player

        self.tool_images = {tool_name: pygame.image.load(f'PydewValley/graphics/overlay/{tool_name}.png').convert_alpha() for tool_name in self.player.tool_list}
        print(self.tool_images)
        self.seed_images = {seed_name: pygame.image.load(f'PydewValley/graphics/overlay/{seed_name}.png').convert_alpha() for seed_name in self.player.seed_list}

    def draw(self, surface):
        img = self.tool_images[self.player.selected_tool]
        rect = img.get_frect(midbottom = OVERLAY_POSITIONS['tool'])
        surface.blit(img, rect)
        