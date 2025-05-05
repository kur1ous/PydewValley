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

def import_folder_dict(folder):
    surface_dict = {}

    for f in os.scandir(folder):
        img = pygame.image.load(f.path).convert_alpha()
        file_name = f.name.split(".")[0]
        surface_dict[file_name] = img
    return surface_dict

# import_assets("PydewValley/graphics/character/")

# print(import_assets("PydewValley/graphics/character"))
