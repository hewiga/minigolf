import pygame
from ball import *
from map import *
from obstacle import *
from main import *

class Game:
    def __init__(self, map_name):
        self.map = Map(map_name, 0)
    
        self.camera_pos = 0
        self.toolbar_rect = pygame.Rect(0, 0, settings.WINDOWS_WIDTH, 3 * settings.OBJECT_SIZE)
        self.workspace_sprites = [pygame.sprite.Group()]
        self.screen_speed = 0

        self.shots_couter = 0
        self.shots_couter_text = Text_Sprite("Shots: " + str(self.shots_couter), (200, self.toolbar_rect.height / 2))
        self.quit_button = Obstacle(settings.sprites['quit'], (settings.WINDOWS_WIDTH - 100, self.toolbar_rect.height / 2), False)
        self.reset_button = Obstacle(settings.sprites['reset'], (settings.WINDOWS_WIDTH - 200, self.toolbar_rect.height / 2), False)

        self.workspace_sprites = self.map.prepare_map(self.workspace_sprites)
        
        self.set_camera_pos(-self.map.ball_pos[0])
        self.ball = Ball(self.map.ball_pos)

        self.ball_direction = 0

    def display_view(self, dt, window):
        current_chunk = int(-self.camera_pos / settings.WINDOWS_WIDTH)
        ball_chunk = 0
        if self.ball.velocity.x > 0:
            ball_chunk = int((-self.camera_pos + self.ball.rect.right) / settings.WINDOWS_WIDTH)
        else:
            ball_chunk = int((-self.camera_pos + self.ball.rect.left) / settings.WINDOWS_WIDTH)

        #draw elements on screen
        self.workspace_sprites[current_chunk].draw(window)
        if current_chunk + 1 < len(self.workspace_sprites): #check current chunk isnt also the last one
            #if not then draw next one
            self.workspace_sprites[current_chunk + 1].draw(window)

        self.handle_camera(current_chunk)
        self.draw_ball(window, ball_chunk, dt)
        
        pygame.draw.rect(window, (0, 0, 0), self.toolbar_rect)
        window.blit(self.shots_couter_text.image, self.shots_couter_text.rect)
        window.blit(self.quit_button.image, self.quit_button.rect)
        window.blit(self.reset_button.image, self.reset_button.rect)

    def set_camera_pos(self, new_pos):
        #this function moves camera to given position
        new_pos_chunk = int(-new_pos / settings.WINDOWS_WIDTH)
        current_chunk = int(-self.camera_pos / settings.WINDOWS_WIDTH)

        #align camera
        align = -self.camera_pos % settings.WINDOWS_WIDTH
        self.camera_pos += align
        self.workspace_sprites[current_chunk].update(align)
        try:
            self.workspace_sprites[current_chunk + 1].update(align)
        except:
            self.workspace_sprites[current_chunk - 1].update(align)

        #check direction
        i = 1
        if self.camera_pos > new_pos:
            #if screen has to go right
            i = -1
        else:
            #if screen has to go left
            i = 1

        while current_chunk != new_pos_chunk:
            self.workspace_sprites[current_chunk].update(settings.WINDOWS_WIDTH * i)
            self.workspace_sprites[current_chunk - i].update(settings.WINDOWS_WIDTH * i)
            self.camera_pos += (settings.WINDOWS_WIDTH * i)
            current_chunk -= 1 * i

    def draw_ball(self, window, ball_chunk, dt):

        self.ball.update(self.workspace_sprites[ball_chunk], dt)
        if self.ball.ready_to_shoot == True:
            pygame.draw.line(window, (0,0,0), self.ball.rect.center, self.ball.direction_coords, 3)
        window.blit(self.ball.image, self.ball.rect)


    def handle_camera(self, current_chunk):

        if self.ball_direction == 0:
            if self.ball.rect.centerx > settings.WINDOWS_WIDTH - (settings.WINDOWS_WIDTH / 5):
                #ball going right
                self.ball_direction = -1
            elif self.ball.rect.centerx < settings.WINDOWS_WIDTH / 5:
                #ball going left
                self.ball_direction = 1
        else:
            if (self.ball_direction == 1 and self.ball.velocity.x > 0 or
            self.ball_direction == -1 and self.ball.velocity.x < 0):
                #if ball hit something and changed direction
                self.ball_direction = 0
                return

            if self.camera_pos == 0 and self.ball_direction == 1:
                self.ball_direction = 0
                return
            elif self.camera_pos == -self.map.farest_object - (settings.OBJECT_SIZE / 2) + settings.WINDOWS_WIDTH and self.ball_direction == -1:
                self.ball_direction = 0     
                return
            
            screen_speed = int(-self.ball.velocity.x) * 2
            if screen_speed == 0:
                screen_speed = self.ball_direction
            

            self.camera_pos += screen_speed
            new_chunk = int(-self.camera_pos / settings.WINDOWS_WIDTH)
            screen_speed = self.align_camera(screen_speed)
            if current_chunk != new_chunk:
                screen_speed = self.align_chunks(screen_speed, current_chunk)
                if screen_speed > 0:
                    return

            self.ball.rect.centerx += screen_speed
            self.ball.position.x += screen_speed
            self.workspace_sprites[current_chunk].update(screen_speed)
            if current_chunk + 1 < len(self.workspace_sprites):
                self.workspace_sprites[current_chunk + 1].update(screen_speed)

            if (self.ball.rect.centerx < settings.WINDOWS_WIDTH / 2 and self.ball_direction == -1 or
            self.ball.rect.centerx > settings.WINDOWS_WIDTH / 2 and self.ball_direction == 1):
                self.ball_direction = 0

    def align_camera(self, screen_speed):
        #align camera to the borders of the map
        if self.camera_pos > 0:
            #aligne to the beginning of the map
            new_screen_speed = screen_speed + (self.camera_pos / -1)
            self.camera_pos = 0
            return new_screen_speed
        
        if self.camera_pos < -self.map.farest_object - (settings.OBJECT_SIZE / 2) + settings.WINDOWS_WIDTH:
            #aligne to the end of the map
            new_screen_speed = screen_speed + (-self.camera_pos + (self.map.farest_object + (settings.OBJECT_SIZE / 2)))
            self.camera_pos = self.map.farest_object + (settings.OBJECT_SIZE / 2)
            return new_screen_speed
        return screen_speed

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

    def handle_mouse(self, asd):
        self.ball.show_direction()

    def handle_action(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y < self.quit_button.rect.bottom:
            if self.quit_button.rect.collidepoint(mouse_x, mouse_y):
                #return to menu
                screen.background_color = (0, 202, 0)
                screen.screen = menu.Menu()
            elif self.reset_button.rect.collidepoint(mouse_x, mouse_y):
                #reset game
                self.set_camera_pos(-self.map.ball_pos[0])
                self.ball.position.update(self.ball.start_pos)
                self.ball.rect.center = self.ball.start_pos
                self.ball.velocity.update(0, 0)
                self.shots_couter = 0
                self.shots_couter_text = Text_Sprite("Shots: " + str(self.shots_couter), (200, self.toolbar_rect.height / 2))
                self.ball.ready_to_shoot = 0
        else:
            if self.ball.ready_to_shoot == True:
                self.shots_couter += 1
                self.shots_couter_text = Text_Sprite("Shots: " + str(self.shots_couter), (200, self.toolbar_rect.height / 2))
                self.ball.set_movement()
