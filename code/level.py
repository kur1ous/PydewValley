import pygame 
from player import Player
from settings import *
from mytimer import Timer
from overlay import Overlay
from cameragroup import CameraGroup
from sprites import Generic, Water, Wildflower, Tree
import pytmx 
from pytmx.util_pygame import load_pygame
from support import import_folder


class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()

		apple_image = pygame.image.load('PydewValley/graphics/fruit/apple.png')

		tmx_data = load_pygame('PydewValley/Data/map.tmx')

		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x, y, img in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE, y * TILE_SIZE), img, LAYERS['house bottom'], self.all_sprites)
	
		for layer in ['HouseWalls', 'HouseFurnitureTop', 'Fence']:
			for x, y, img in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x*TILE_SIZE, y*TILE_SIZE), img, LAYERS['main'], [self.all_sprites, self.collision_sprites])
		
		for layer in ['Collision']:
			for x, y, img in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x*TILE_SIZE, y*TILE_SIZE), img, LAYERS['main'], self.collision_sprites)

		water_frames = import_folder("PydewValley/graphics/water")
		for x, y, img in tmx_data.get_layer_by_name('Water').tiles():
			Water((x*TILE_SIZE, y*TILE_SIZE), water_frames, self.all_sprites)

		for obj in tmx_data.get_layer_by_name('Decoration'):
			Wildflower((obj.x, obj.y), obj.image, self.all_sprites)

		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree((obj.x, obj.y), obj.image, obj.name, apple_image, [self.all_sprites, self.collision_sprites, self.tree_sprites])

			
		ground_image = pygame.image.load("PydewValley/graphics/world/ground.png").convert_alpha()
		Generic((0,0), ground_image, LAYERS['ground'], self.all_sprites)

		self.player = Player((1547.813354, 1943.214233), pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT, pygame.K_e, pygame.K_r, pygame.K_q, pygame.K_LCTRL, self.collision_sprites, self.tree_sprites, self.all_sprites, )
		self.overlay = Overlay(self.player)


	def run(self,dt):
		self.display_surface.fill('black')
		self.all_sprites.draw(self.display_surface, (self.player.rect.center))
		self.all_sprites.update(dt)
		self.overlay.draw(self.display_surface)
		

