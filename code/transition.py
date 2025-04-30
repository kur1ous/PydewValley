import pygame
from settings import *

class Transition:

    def __init__(self, player, callback):
        self.player = player
        self.callback = callback

        self.display_surface = pygame.display.get_surface()

        self.FADE = "fading out"
        self.UNFADE = "fading in"
        self.INACTIVE = "inactive"
        self.status = self.INACTIVE

        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.alpha = 0
        self.speed = 200

    def start(self):
        self.status = self.FADE
        self.player.lock_input()
        self.alpha = 0

    def draw(self):
        if self.status == self.INACTIVE: return
        self.image.set_alpha(int(self.alpha))
        self.display_surface.blit(self.image, (0,0))
        
    def update(self, dt):
        if self.status == self.FADE:
            self.alpha += self.speed * dt
            if self.alpha >= 225:
                self.alpha = 255
                self.status = self.UNFADE
                self.callback()
        if self.status == self.UNFADE:
            self.alpha -= self.speed * dt
            if self.alpha <= 0:
                self.alpha = 0
                self.status = self.INACTIVE
                self.player.unlock_input()