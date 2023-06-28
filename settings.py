from os import listdir
import pygame

OBJECT_SIZE = 64
WINDOWS_WIDTH = 1920
WINDOWS_HEIGHT = 1080

sprites = {}

def load_sprites():
    for element in listdir('sprites/'):
        sprites[element.split('.')[0]] = pygame.image.load('sprites/' + element).convert_alpha()