from django.conf import settings
import pygame, settings


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, sprite_name, pos, angle = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_name
        self.rect = self.image.get_rect(center = pos)
        self.basic_rect = self.rect
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = angle
        
    def update(self, camera_pos):

        self.rect.centerx = self.basic_rect.centerx + camera_pos