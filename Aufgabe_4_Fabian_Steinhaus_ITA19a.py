import pygame
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_DOWN)
import os
import random
import time

class Settings(object):
    def __init__(self):
        self.width = 750
        self.height = 400
        self.fps = 60 
        self.title = "Steinhaus Aufgabe 4"       
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.file_path, "images")

    def get_dim(self):
        return (self.width, self.height)

class Blase(pygame.sprite.Sprite):
    def __init__(self, pygame):
        pygame.sprite.Sprite.__init__(self)
        self.pygame = pygame
        self.settings = settings
        self.time = time.time()
        self.imageOriginal = pygame.image.load(os.path.join(self.settings.images_path, "blase3.png")).convert_alpha()
        self.image = pygame.transform.scale(self.imageOriginal, (10, 10))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.top = random.randint(1, 500)
        self.rect.left = random.randint(1, 300)
        self.scale = 5

    def scaleBlase(self):
        self.timeNow = time.time()
        if (self.timeNow - self.time) >= 1:
            self.time = time.time()
            self.scale += 5
            self.image = self.pygame.transform.scale(self.imageOriginal, (self.scale, self.scale))
            self.mask = pygame.mask.from_surface(self.image)


class Game():
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.pygame.display.set_caption(self.settings.title)
        self.screen = pygame.display.set_mode(self.settings.get_dim())
        self.clock = pygame.time.Clock()
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path, "nature.jpg")).convert()
        self.background = self.pygame.transform.scale(self.background, (self.settings.get_dim()))
        self.background_rect = self.background.get_rect()
        self.done = False
        self.blase_01 = Blase(self.pygame)
        self.blase_02 = Blase(self.pygame)
        self.blase_03 = Blase(self.pygame)
        self.alleBlasen = pygame.sprite.Group()
        self.alleBlasen.add(self.blase_01, self.blase_02, self.blase_03)
        self.cursor = self.pygame.image.load(os.path.join(self.settings.images_path, "blase10x10.png")).convert_alpha()
        self.pygame.mouse.set_visible(False)  
        self.rect = self.cursor.get_rect()
        self.mask = self.pygame.mask.from_surface(self.cursor)

    def updateMouse(self):
        self.mousePos = self.pygame.mouse.get_pos()
        self.screen.blit(self.cursor, self.mousePos)
        self.rect = self.cursor.get_rect()
        self.mask = self.pygame.mask.from_surface(self.cursor) 



    def run(self):
        while not self.done:
            self.clock.tick(self.settings.fps)
            for event in self.pygame.event.get():
                if event.type == QUIT:
                    self.done = True   
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True

            self.screen.blit(self.background,(self.background_rect))
            self.alleBlasen.draw(self.screen)
            self.blase_01.scaleBlase()
            self.blase_02.scaleBlase()
            self.blase_03.scaleBlase()
            self.updateMouse()
            self.pygame.display.flip()

if __name__ == '__main__':                                
    settings = Settings()
    pygame.init()             
    game = Game(pygame, settings)
    game.run()
    pygame.quit() 