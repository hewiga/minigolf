import pygame, settings
from editor import *
from game import *
from text_sprite import *

class Level_select:
    def __init__(self, edition):
        self.edition = edition
        self.map_name = ''
        self.communique = Text_Sprite('Type map name:', (settings.WINDOWS_WIDTH / 2, 200))
        self.map_name_sprite = Text_Sprite(self.map_name, (settings.WINDOWS_WIDTH / 2, 400))
    def __str__(self):   
        return "Level selector"

    def display_view(self, dt, window):

        window.blit(self.communique.image, self.communique.rect)
        window.blit(self.map_name_sprite.image, self.map_name_sprite.rect)

    def handle_mouse(self, dt):
        return
    
    def handle_action(self, screen, key):
        if key >= 97 and key <= 122:
            self.map_name += chr(key)
            self.map_name_sprite = Text_Sprite(self.map_name, (settings.WINDOWS_WIDTH / 2, 400))
        elif key == 8:
            self.map_name = self.map_name[:-1]
            self.map_name_sprite = Text_Sprite(self.map_name, (settings.WINDOWS_WIDTH / 2, 400))
        elif key == 13:
            
            if len(self.map_name) != 0:
                self.map_name = "maps/" + self.map_name + ".txt"
                if self.edition:
                    screen.screen = Editor(self.map_name)
                    screen.background_color = (91, 198, 255)
                else:
                    screen.screen = Game(self.map_name)
                    screen.background_color = (91, 198, 255)