import pygame, settings
from map import *
from obstacle import *
import menu

class Editor:
    def __init__(self, map_name):
        self.map = Map(map_name, 1)
        self.camera_pos = 0

        self.toolbar_rect = pygame.Rect(0, 0, settings.WINDOWS_WIDTH, 3 * settings.OBJECT_SIZE)
        self.save_button = Obstacle(settings.sprites['save'], (settings.WINDOWS_WIDTH - 200, self.toolbar_rect.height / 2), False)
        self.quit_button = Obstacle(settings.sprites['quit'], (settings.WINDOWS_WIDTH - 100, self.toolbar_rect.height / 2), False)
        self.current_block = Obstacle(settings.sprites['obstacle1'], (settings.WINDOWS_WIDTH - 300, self.toolbar_rect.height / 2), False)
        
        self.current_block_num = 1
        self.workspace_sprites = [pygame.sprite.Group()]
        

        self.workspace_sprites = self.map.prepare_map(self.workspace_sprites)
        self.toolbar_sprites = pygame.sprite.Group()
        self.prepare_toolbar()

    def __str__(self):
        return "Editor"

    def prepare_toolbar(self):

        #load all sprites and put them on toolbar
        for i in range(7):
            sprite_name = settings.sprites['obstacle' + str(i + 1)]
            icon = Obstacle(sprite_name, (128 * (i+1), self.toolbar_rect.height / 2), False)
            self.toolbar_sprites.add(icon)
        icon = Obstacle(settings.sprites['ball'], ((128 * 8), self.toolbar_rect.height / 2), False)
        self.toolbar_sprites.add(icon)

    def display_view(self, dt, window):
        current_chunk = int(-self.camera_pos / settings.WINDOWS_WIDTH)
        self.workspace_sprites[current_chunk].draw(window)
        if current_chunk + 1 < len(self.workspace_sprites): #check current chunk isnt also the last one
            #if not then draw next one
            self.workspace_sprites[current_chunk + 1].draw(window)

        pygame.draw.rect(window, (0, 0, 0), self.toolbar_rect)
        self.toolbar_sprites.draw(window)
        window.blit(self.current_block.image, self.current_block.rect)
        window.blit(self.save_button.image, self.save_button.rect)
        window.blit(self.quit_button.image, self.quit_button.rect)

    def handle_mouse(self, dt):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y <= self.toolbar_rect.height: #if mouse is on toolbar then return
            return

        if mouse_x > settings.WINDOWS_WIDTH - (settings.WINDOWS_WIDTH / 10): #if mouse is on the right side of the screen then move it right
            self.move_camera(-dt)

        elif mouse_x < settings.WINDOWS_WIDTH / 10: #move left
            self.move_camera(dt)

    def move_camera(self, dt):

        current_chunk = int(-self.camera_pos / settings.WINDOWS_WIDTH)
        camera_move = 1000 * dt
        self.camera_pos += camera_move
        new_chunk = int(-self.camera_pos / settings.WINDOWS_WIDTH)

        camera_move = self.align_camera(camera_move)
        if current_chunk != new_chunk:
            camera_move = self.align_chunks(camera_move, current_chunk)
            if camera_move > 0:
                return

        self.workspace_sprites[current_chunk].update(camera_move)
        if current_chunk + 1 < len(self.workspace_sprites):
            self.workspace_sprites[current_chunk + 1].update(camera_move)

    def align_camera(self, camera_move):
        if self.camera_pos > 0: 
            #align camera to start
            camera_move += self.camera_pos / -1 #if camera is lower than zero than add the difference
            self.camera_pos = 0                 #then set camera position as 0
        elif self.camera_pos < -(self.map.farest_object - (settings.OBJECT_SIZE / 2)):
            self.camera_pos -= camera_move
            camera_move = 0 
        return camera_move

    def align_chunks(self, camera_move, current_chunk):
        if camera_move < 0:
        #if camera is going right
                aligned_camera = (-self.camera_pos % settings.WINDOWS_WIDTH)
                camera_move += aligned_camera
                self.camera_pos += aligned_camera
        else:
        #if camera is going left
            aligned_camera = (current_chunk * settings.WINDOWS_WIDTH) + self.camera_pos
            asd = camera_move - aligned_camera
            self.workspace_sprites[current_chunk - 1].update(aligned_camera)
            self.workspace_sprites[current_chunk].update(camera_move)
            if current_chunk + 1 < len(self.workspace_sprites):
                self.workspace_sprites[current_chunk + 1].update(asd)

        return camera_move

    def add_object(self, mouse_x, mouse_y):
        
        current_chunk = int((mouse_x - self.camera_pos) / settings.WINDOWS_WIDTH)
        pos_x = (int((mouse_x - (self.camera_pos % settings.OBJECT_SIZE)) / settings.OBJECT_SIZE) * settings.OBJECT_SIZE + int(settings.OBJECT_SIZE / 2)) + (self.camera_pos % settings.OBJECT_SIZE)
        pos_y = (int(mouse_y / settings.OBJECT_SIZE) * settings.OBJECT_SIZE + int(settings.OBJECT_SIZE / 2)) 

        editor_data_pos_x = int((-self.camera_pos + mouse_x) / settings.OBJECT_SIZE)
        editor_data_pos_y = int((mouse_y - (3 * settings.OBJECT_SIZE)) / settings.OBJECT_SIZE)

        #extend editor data if needed 
        if len(self.map.map_editor_data[editor_data_pos_y]) <= editor_data_pos_x:
            difference = editor_data_pos_x - len(self.map.map_editor_data[editor_data_pos_y])
            for x in range(difference + 1):
                self.map.map_editor_data[editor_data_pos_y].append(0)
            
        self.map.map_editor_data[editor_data_pos_y][editor_data_pos_x] = self.current_block_num

        #extend array if necessary
        if current_chunk >= len(self.workspace_sprites):
            self.workspace_sprites.append(pygame.sprite.Group())

        #check if any element doesnt exist at this coords already
        for element in self.workspace_sprites[current_chunk].sprites():
            #if is then just change its sprite
            if element.rect.collidepoint(pos_x, pos_y):
                element.image = self.current_block.image
                return
        
        #else create new object and put it in right place
        new_platform = Obstacle(self.current_block.image, (pos_x, pos_y))
        self.workspace_sprites[current_chunk].add(new_platform)

        #check if object isnt the farest one so the map could scroll further 
        if pos_x - self.camera_pos > self.map.farest_object:
            self.map.farest_object = pos_x - self.camera_pos

    def delete_object(self, mouse_x, mouse_y):
        current_chunk = int((mouse_x + -self.camera_pos) / settings.WINDOWS_WIDTH)
        pos_x = (int((mouse_x - (self.camera_pos % settings.OBJECT_SIZE)) / settings.OBJECT_SIZE) * settings.OBJECT_SIZE + int(settings.OBJECT_SIZE / 2)) + (self.camera_pos % settings.OBJECT_SIZE)
        pos_y = (int(mouse_y / settings.OBJECT_SIZE) * settings.OBJECT_SIZE + int(settings.OBJECT_SIZE / 2)) 
    
        editor_data_pos_x = int((-self.camera_pos + mouse_x) / settings.OBJECT_SIZE)
        editor_data_pos_y = int((mouse_y - (3 * settings.OBJECT_SIZE)) / settings.OBJECT_SIZE)

        if len(self.map.map_editor_data[editor_data_pos_y]) <= editor_data_pos_x:
            return
        else:
            self.map.map_editor_data[editor_data_pos_y][editor_data_pos_x] = 0

        for element in self.workspace_sprites[current_chunk].sprites():
            if element.rect.collidepoint(pos_x, pos_y):
                element.kill()

    def handle_action(self, screen):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        block_num = 1
        if mouse_y < self.toolbar_rect.height:  
            #if mouse is on toolbar
            for element in self.toolbar_sprites.sprites():  #check if any icon on toolbar was clicked
                if element.rect.collidepoint(mouse_x, mouse_y):
                    self.current_block.image = element.image
                    self.current_block_num = block_num
                block_num += 1
            if self.save_button.rect.collidepoint(mouse_x, mouse_y):
                self.map.save()
            elif self.quit_button.rect.collidepoint(mouse_x, mouse_y):
                screen.background_color = (0, 202, 0)
                screen.screen = menu.Menu()
        else: 
            #if mouse is in workspace
            if pygame.mouse.get_pressed()[0]:
                self.add_object(mouse_x, mouse_y)
            elif pygame.mouse.get_pressed()[2]:
                self.delete_object(mouse_x, mouse_y)
