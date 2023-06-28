import pygame, sys, settings
from text_sprite import *
from level_select import Level_select

class Menu:
    def __init__(self):
        
        self.logo = settings.sprites['logo']
        self.all_sprites = pygame.sprite.Group()
        self.window_center = pygame.display.get_window_size()[0] / 2

        self.all_sprites.add(Text_Sprite("Play", (self.window_center, 600)))        
        self.all_sprites.add(Text_Sprite("Create Level", (self.window_center, 700)))      
        self.all_sprites.add(Text_Sprite("Exit", (self.window_center, 800)))      
        self.sprites = self.all_sprites.sprites()

    def display_view(self, dt, window):
        window.blit(self.logo, (self.window_center - (self.logo.get_rect().width / 2), 200))
        self.all_sprites.draw(window)        

    def handle_mouse(self, dt):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        for sprite in self.sprites:
            if sprite.rect.collidepoint(mouse_pos_x, mouse_pos_y):
                sprite.activate()
                break
            elif sprite.is_active == 1:
                sprite.unactivate()

    def handle_action(self, screen):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if self.sprites[0].rect.collidepoint(mouse_pos_x, mouse_pos_y):
            #PLAY button
            screen.screen = Level_select(0)
            
        if self.sprites[1].rect.collidepoint(mouse_pos_x, mouse_pos_y):
            #EDITOR button
            screen.screen = Level_select(1)

        if self.sprites[2].rect.collidepoint(mouse_pos_x, mouse_pos_y):
            #EXIT button
            pygame.quit()
            sys.exit()