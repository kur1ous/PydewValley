import pygame 
from player import Player
from settings import *
from mytimer import Timer
from overlay import Overlay

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = pygame.sprite.Group()

		self.player = Player((50,200), pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT, pygame.K_e, pygame.K_r, pygame.K_q, pygame.K_LCTRL, self.all_sprites)
		self.overlay = Overlay(self.player)


	def run(self,dt):
		self.display_surface.fill('black')
		self.all_sprites.draw(self.display_surface)
		self.all_sprites.update(dt)
		self.overlay.draw(self.display_surface)

