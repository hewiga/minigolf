import pygame, settings, menu

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.image = settings.sprites['ball']

        self.start_pos = [pos[0] % settings.WINDOWS_WIDTH, pos[1]]
        self.rect = self.image.get_rect(center = self.start_pos)
        self.ball_angle = 0
        self.was_collision = False
        self.ready_to_shoot = False

        self.mask = pygame.mask.from_surface(self.image)


        self.direction_coords = pygame.Vector2(0, 0)

        self.FRICTION_Y = 2
        self.FRICTION_X = .05
        self.GRAVITY = 1

        self.position = pygame.Vector2(self.start_pos)
        self.velocity = pygame.Vector2(0, 0)

    def update(self, sprites, dt):
        
        if not self.ready_to_shoot:
            
            self.horizontal_movement(dt)
            self.vertical_movement(dt)
            self.check_collision(sprites, dt)

            if self.velocity.x == 0 and self.velocity.y == 0:
                self.ready_to_shoot = True


    def horizontal_movement(self, dt):

        if self.velocity.x > 0: #if ball is moving right
            self.velocity.x -= self.FRICTION_X * dt
            #ball is moving right so if its trying to go left becouse of FRICTION_X it means it should stop
            if self.velocity.x < 0:
                self.velocity.x = 0
        elif self.velocity.x < 0: #if ball is moving left
            self.velocity.x += self.FRICTION_X * dt
            #same case as above
            if self.velocity.x > 0:
                self.velocity.x = 0
        
        self.position.x += self.velocity.x
        self.rect.centerx = self.position.x

    def vertical_movement(self, dt):
        
        self.velocity.y += self.GRAVITY * dt
        if self.velocity.y < 0:
            self.velocity.y += self.FRICTION_Y * dt

        self.position.y += self.velocity.y
        self.rect.centery = self.position.y

    def set_movement(self):

        x_diff = self.direction_coords.x - self.rect.centerx
        y_diff = self.direction_coords.y - self.rect.centery
        
        self.velocity.x = x_diff / 90
        self.velocity.y = y_diff / 70
        self.ready_to_shoot = False
        self.was_collision = False

    def check_collision(self, sprites, dt): 
        
        if self.rect.left <= 0 or self.rect.right >= settings.WINDOWS_WIDTH:
            self.velocity.x *= -1
            self.velocity.x *= .5
            
        for sprite in sprites.sprites():
            if not sprite.angle:
                if self.collision_rect(sprite, dt):
                    self.collision_mask(sprite)
                    break
            else:
                if self.collision_mask(sprite):
                    break
    
    def collision_rect(self, sprite, dt):

        collision_tolerance = 5
        if self.rect.colliderect(sprite.rect):
            if abs(self.rect.top - sprite.rect.bottom) < collision_tolerance:
                self.velocity.y *= -1
                self.velocity.y *= .5
                self.rect.top = sprite.rect.bottom
                self.position.y = self.rect.centery

            elif abs(self.rect.bottom - sprite.rect.top) < collision_tolerance:

                self.velocity.y -= self.FRICTION_Y * dt
                if self.velocity.y <= 0.05:
                    self.velocity.y = 0
                    self.rect.bottom = sprite.rect.top
                    self.position.y = self.rect.centery
                else:
                    self.velocity.y *= -1
                    self.velocity.x *= .9


            elif abs(self.rect.right - sprite.rect.left) < collision_tolerance:
                self.rect.right = sprite.rect.left
                self.position.x = self.rect.centerx
                self.velocity.x *= -1
                self.velocity.x *= .5

            elif abs(self.rect.left - sprite.rect.right) < collision_tolerance:
                self.rect.left = sprite.rect.right
                self.position.x = self.rect.centerx
                self.velocity.x *= -1
                self.velocity.x *= .5
            return 1
        return 0

    def collision_mask(self, sprite):
        if pygame.sprite.collide_mask(self, sprite):
            asd = pygame.sprite.collide_mask(self, sprite)
            asd = pygame.Vector2(asd)
            if not sprite.angle:
                return 0
            angle = asd.angle_to(pygame.Vector2(0,0))
            self.velocity.rotate_ip(angle*2)
            return 1
        return 0

    def show_direction(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse_x - self.rect.centerx, mouse_y - self.rect.centery)
        if direction.length() > 200:
            direction.scale_to_length(200)
            self.direction_coords.update(direction + self.rect.center)
        else:
            self.direction_coords.update(mouse_x, mouse_y)