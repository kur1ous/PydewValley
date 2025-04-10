import pygame
import os
from settings import *

def import_assets(folder):
    assets = {}
    for f in os.scandir(folder):
        if f.is_dir():
            assets[f.name] = import_folder(f.path)
    return assets

def import_folder(folder):
    images = []
    for f in os.scandir(folder):
        if not f.is_dir():
            img = pygame.image.load(f.path).convert_alpha()
            images.append(img)
    return images

# import_assets("PydewValley/graphics/character/")

# print(import_assets("PydewValley/graphics/character"))
