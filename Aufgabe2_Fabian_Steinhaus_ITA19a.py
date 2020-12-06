import pygame
import random
from pygame.constants import (
    QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_DOWN)
import sys
import os


class Settings(object):
    def __init__(self):
        self.width = 750
        self.height = 450
        self.fps = 60       
        self.title = "Steinhaus Aufgabe2" 
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.file_path, "images")

    def get_dim(self):
        return (self.width, self.height)

class Defender(pygame.sprite.Sprite):
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "defender_astro90.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 42))
        self.rect = self.image.get_rect()
        self.rect.left = (settings.width - self.rect.width) // 2
        self.rect.top = settings.height - self.rect.height - 10
        self.direction = 0
        self.direction_top = 0
        self.speed = 8

    def update(self):
        newleft = self.rect.left + (self.direction * self.speed)
        newhigh = self.rect.top + (self.direction_top * self.speed)
        newright = newleft + self.rect.width
        newdown = newhigh + self.rect.height
        if newleft > 0 and newright < settings.width:
            self.rect.left = newleft
        if newhigh > 0 and newdown < settings.height:
            self.rect.top = newhigh

class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path, "weltraum8.png")).convert()
        self.background_rect = self.background.get_rect()
        self.defender = Defender(settings)
        self.clock = pygame.time.Clock()
        self.done = False
        self.all_defenders = pygame.sprite.Group()
        self.all_defenders.add(self.defender)

    def run(self):
        while not self.done:  
            self.clock.tick(self.settings.fps)  
            for event in self.pygame.event.get():
                if event.type == QUIT:     
                    self.done = True             
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True
                    if event.key == K_LEFT:
                        self.defender.direction = -1
                    if event.key == K_SPACE:
                        self.defender.rect.left = random.randrange(50, 700)
                        self.defender.rect.top = random.randrange(50, 400)
                    elif event.key == K_RIGHT: 
                        self.defender.direction = 1
                    elif event.key == K_UP:
                        self.defender.direction_top = -1
                    elif event.key == K_DOWN:
                        self.defender.direction_top  = 1
                elif event.type == KEYUP: 
                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:          
                        self.defender.direction = 0
                        self.defender.direction_top = 0
     
                
            self.update()
            self.draw()
 
    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        self.all_defenders.draw(self.screen)
        self.pygame.display.flip()

    def update(self):
        self.all_defenders.update()


if __name__ == '__main__':      
    settings = Settings()
    pygame.init() 
    game = Game(pygame, settings)
    game.run()
    pygame.quit()          

