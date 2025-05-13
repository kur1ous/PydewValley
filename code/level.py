import pygame 
from player import Player
from settings import *
from mytimer import Timer
from overlay import Overlay
from cameragroup import CameraGroup
from sprites import Generic, Water, Wildflower, Tree, Interaction, FallingDrops
from transition import  Transition
import pytmx 
from pytmx.util_pygame import load_pygame
from support import import_folder
from soil import SoilLayer
from weather import Rain
import random

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()
		self.soil_layer = SoilLayer(self.all_sprites)

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


			
			
		ground_image = pygame.image.load("PydewValley/graphics/world/ground.png").convert_alpha()
		Generic((0,0), ground_image, LAYERS['ground'], self.all_sprites)

		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Bed':
				self.bed = Interaction((obj.x, obj.y), (obj.width, obj.height), obj.name, [self.interaction_sprites])
			if obj.name == 'Start':
				self.player = Player((obj.x, obj.y), pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT, pygame.K_e, pygame.K_r, pygame.K_q, pygame.K_LCTRL, self.collision_sprites, self.tree_sprites, self.interaction_sprites, self.use_bed, self.soil_layer, self.all_sprites)
		
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree((obj.x, obj.y), obj.image, obj.name, apple_image, self.player.add_item, [self.all_sprites, self.collision_sprites, self.tree_sprites])

		self.overlay = Overlay(self.player)

		# rain
		self.raining = False
		self.rain = Rain(self.all_sprites)


		self.next_day_transition = Transition(self.player, self.next_day)

	def next_day(self):
		for tree in self.tree_sprites:
			tree.reset()
		self.soil_layer.grow_plnats()

		self.soil_layer.remove_water()
		self.raining = random.randint(0,10) < 2
		if self.raining:
			self.soil_layer.water_all()


	def use_bed(self):
		self.next_day_transition.start()

	def plant_collision(self):
		for plant in self.soil_layer.plant_sprites:
			if plant.hitbox.colliderect(self.player.hitbox):


				self.soil_layer.harvest(plant, self.player.add_item)

	def run(self,dt):
		self.display_surface.fill('black')
		self.all_sprites.draw(self.display_surface, (self.player.rect.center), self.soil_layer.grid)
		self.all_sprites.update(dt)
		self.overlay.draw(self.display_surface)
		self.next_day_transition.update(dt)
		self.next_day_transition.draw()

		if self.raining:
			self.rain.update()

		self.plant_collision()
		

