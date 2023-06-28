from platform import platform
import pygame, settings
from obstacle import *

class Map():
    def __init__(self, map_name, edition):
        self.map_name = map_name
        self.map_data = ''
        self.farest_object = 0
        self.map_chunk = 0
        self.current_x = 0
        self.edition = edition

        self.ball_pos = [0, 0]

        try: 
            with open(self.map_name, 'r') as map:
                self.map_data = map.read()
        except:
            self.map_data = ''

        if self.edition:    
            self.map_editor_data = []
            for x in range(14):
                self.map_editor_data.append([])

    def prepare_map(self, sprites):
        self.current_x = settings.OBJECT_SIZE / 2
        current_y = settings.OBJECT_SIZE / 2 + settings.OBJECT_SIZE * 3
        editor_data_y = 0

        for object in self.map_data:
            if object == '\n':
                current_y += settings.OBJECT_SIZE
                self.current_x = settings.OBJECT_SIZE / 2
                self.map_chunk = 0
                if self.edition:
                    editor_data_y += 1
                continue

            elif object == ' ':
                self.current_x += settings.OBJECT_SIZE
                sprites = self.extend_map(sprites)
                if self.edition:
                    self.map_editor_data[editor_data_y].append(0)
                continue
            elif object == '8':
                if self.edition:
                    platform = Obstacle(settings.sprites['ball'], (self.current_x, current_y), True)
                else:
                    self.ball_pos = [self.current_x + ((self.map_chunk - 1) * settings.WINDOWS_WIDTH), current_y]
                    self.current_x += settings.OBJECT_SIZE
                    continue       
            else:
                name_of_obstacle = 'obstacle' + object
                angel = False
                if object == '3' or object == '5' or object == '7':
                    angel = True
                platform = Obstacle(settings.sprites[name_of_obstacle], (self.current_x, current_y), angel)

            sprites[self.map_chunk].add(platform)
            if self.current_x + ((self.map_chunk - 1) * settings.WINDOWS_WIDTH) > self.farest_object:
                self.farest_object = self.current_x + ((self.map_chunk - 1) * settings.WINDOWS_WIDTH)

            if self.edition:
                self.map_editor_data[editor_data_y].append(int(object))

            self.current_x += settings.OBJECT_SIZE
            sprites = self.extend_map(sprites)
        return sprites

    def extend_map(self, sprites):
        
        if self.current_x == (settings.WINDOWS_WIDTH * 2) + (settings.OBJECT_SIZE / 2):
            self.current_x = settings.WINDOWS_WIDTH + (settings.OBJECT_SIZE / 2)
            self.map_chunk += 1
            if self.map_chunk == len(sprites):
                sprites.append(pygame.sprite.Group())
            return sprites
        if self.current_x == settings.WINDOWS_WIDTH + (settings.OBJECT_SIZE / 2):
            self.map_chunk += 1
            if self.map_chunk == len(sprites):
                sprites.append(pygame.sprite.Group())
            return sprites
        return sprites

    def save(self):
        file = open(self.map_name, 'w')
        for y in self.map_editor_data:
            line = ""
            if len(y) == 0:
                file.write('\n')
                continue
            for x in y:
                if x == 0:
                    line += ' '
                    continue
                line += str(x)
            line += '\n'
            file.write(line)