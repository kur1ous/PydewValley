import pygame 
from player import Player
from settings import *
from mytimer import Timer
from overlay import Overlay
from cameragroup import CameraGroup
from sprites import Generic, Water
import pytmx 
from pytmx.util_pygame import load_pygame
from support import import_folder


class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()

		tmx_data = load_pygame('PydewValley/Data/map.tmx')

		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x, y, img in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE, y * TILE_SIZE), img, LAYERS['house bottom'], self.all_sprites)
	
		for j in ['HouseWalls', 'HouseFurnitureTop', 'Fence']:
			for x, y, img in tmx_data.get_layer_by_name(j).tiles():
				Generic((x*TILE_SIZE, y*TILE_SIZE), img, LAYERS['main'], self.all_sprites)

		water_frames = import_folder("PydewValley/graphics/water")
		for x, y, img in tmx_data.get_layer_by_name('Water').tiles():
			Water((x*TILE_SIZE, y*TILE_SIZE), water_frames, self.all_sprites)
			
		ground_image = pygame.image.load("PydewValley/graphics/world/ground.png").convert_alpha()
		Generic((0,0), ground_image, LAYERS['ground'], self.all_sprites)

		self.player = Player((SCREEN_WIDTH/2,SCREEN_HEIGHT/2), pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT, pygame.K_e, pygame.K_r, pygame.K_q, pygame.K_LCTRL, self.all_sprites)
		self.overlay = Overlay(self.player)


	def run(self,dt):
		self.display_surface.fill('black')
		self.all_sprites.draw(self.display_surface, (self.player.rect.center))
		self.all_sprites.update(dt)
		self.overlay.draw(self.display_surface)
		

