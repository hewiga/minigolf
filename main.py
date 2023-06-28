import pygame, sys, settings
from menu import *

class App:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_cursor(pygame.cursors.arrow)

        self.info = pygame.display.Info()
        self.window = pygame.display.set_mode((settings.WINDOWS_WIDTH, settings.WINDOWS_HEIGHT), pygame.FULLSCREEN)
        settings.load_sprites()

        self.clock = pygame.time.Clock()
        self.screen = Menu()
        self.background_color = (0, 202, 0)
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        pygame.quit()
                        sys.exit()
                if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                    if self.screen.__str__() == "Editor":
                        self.screen.handle_action(self)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]: #if left mouse button was pressed
                        self.screen.handle_action(self)

                if self.screen.__str__() == "Level selector":
                    if event.type == pygame.KEYDOWN:
                        self.screen.handle_action(self, event.key)

            self.window.fill(self.background_color)  
            
            dt = self.clock.tick() / 1000
            self.screen.handle_mouse(dt)
            self.screen.display_view(dt, self.window)
            pygame.display.update()

if __name__ == "__main__":

    menu = App()
    menu.run()