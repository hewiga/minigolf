import pygame

class Text_Sprite(pygame.sprite.Sprite):
    def __init__(self, content, pos):
        pygame.sprite.Sprite.__init__(self)
        
        self.sprite_content = content
        self.font = pygame.font.SysFont("Arial", 48)
        self.image = self.font.render(self.sprite_content, True, (255, 255, 255))
        self.rect = self.image.get_rect(center = pos)
        self.is_active = 0

    def activate(self):
        self.image = self.font.render(self.sprite_content, True, (255, 0, 0))
        self.is_active = 1
    
    def unactivate(self):
        self.image = self.font.render(self.sprite_content, True, (255, 255, 255))
        self.is_active = 0