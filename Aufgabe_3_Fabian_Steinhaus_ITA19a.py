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
        self.title = "Steinhaus Aufgabe 3"       
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.file_path, "images")

    def get_dim(self):
        return (self.width, self.height)

class Defender(pygame.sprite.Sprite):
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "defender01.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.left = (settings.width - self.rect.width) // 2
        self.rect.top = (settings.height - self.rect.height) - 10
        self.direction = 0
        self.direction_y = 0
        self.speed = 5

    def update(self):
        newtop = self.rect.top + (self.speed * self.direction)
        newbottom = newtop + self.rect.height
        newleft = self.rect.left + (self.speed * self.direction)
        newright = newleft + self.rect.width

        if newtop <= 0:
            self.direction_y = 0
        if newbottom >= settings.height:
            self.direction_y = 0
        if newleft <= 0:
            self.direction = 0
        if newright >= settings.width:
            self.direction = 0

        self.rect.left = self.rect.left + (self.direction * self.speed) 
        self.rect.top = self.rect.top + (self.direction_y * self.speed)


    def draw(self,screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Astroids(pygame.sprite.Sprite):
    def __init__(self, settings):
        self.settings = settings
        self.directions = [-1, 1]
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "asteroid_big2.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image,(30 ,30))
        self.rect = self.image.get_rect()
        self.speed = random.randint(1, 3)
        self.rect.left = random.randint(1, 720)
        self.rect.top = 0
        self.direction = random.choice(self.directions)
        self.direction_y = 1


    def update(self, defender):
        newtop = self.rect.top + (self.direction_y * self.speed)
        newbottom = newtop + self.rect.height
        newleft = self.rect.left + (self.direction * self.speed)
        newright = newleft + self.rect.width

        if newleft <= 0:
            self.direction = 1
        if newright >= settings.width:
            self.direction = -1
        if newbottom >= settings.height:
            self.rect.left = random.randint(1, 720)
            self.rect.top = random.randint(1, 5)
            self.direction = random.choice(self.directions)

        self.rect.left += (self.direction * self.speed) 
        self.rect.top += (self.direction_y * self.speed)

        if pygame.sprite.collide_mask(defender, self):
            game.done = True

                    

class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.pygame.display.set_caption(self.settings.title)
        self.screen = pygame.display.set_mode(self.settings.get_dim())
        self.clock = pygame.time.Clock()
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path, "weltraum8.png")).convert()
        self.background = self.pygame.transform.scale(self.background, (self.settings.get_dim()))
        self.background_rect = self.background.get_rect()
        self.defender = Defender(self.settings)
        self.all_defender = pygame.sprite.Group()
        self.all_defender.add (self.defender)
        self.create_astroids()
        self.done = False

    def create_astroids(self):
        self.astroid_1 = Astroids(self.settings)
        self.astroid_2 = Astroids(self.settings)
        self.astroid_3 = Astroids(self.settings)
        self.astroid_4 = Astroids(self.settings)
        self.astroid_5 = Astroids(self.settings)
        self.astroid_6 = Astroids(self.settings)
        self.astroid_7 = Astroids(self.settings)
        self.astroid_8 = Astroids(self.settings)
        self.all_astroids = pygame.sprite.Group()
        self.all_astroids.add (self.astroid_1, self.astroid_2, self.astroid_3, self.astroid_4, self.astroid_5, self.astroid_6, self.astroid_7, self.astroid_8)


    def run(self):
        while not self.done:
            self.clock.tick(self.settings.fps)
            for event in self.pygame.event.get():
                if event.type == QUIT:
                    self.done = True   
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True
                    elif event.key == K_LEFT:
                        self.defender.direction = -1
                    elif event.key == K_RIGHT:
                        self.defender.direction = 1 
                    elif event.key == K_UP:
                        self.defender.direction_y = -1
                    elif event.key == K_DOWN:
                        self.defender.direction_y = 1
                elif event.type == KEYUP: 
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        self.defender.direction = 0
                    elif event.key == K_UP or event.key == K_DOWN:
                        self.defender.direction_y = 0
                    elif event.key == K_SPACE:
                        self.defender.rect.top = random.randint(1,350)
                        self.defender.rect.left = random.randint(1,720)

            self.defender.update()
            self.all_astroids.update(self.defender)             
            self.screen.blit(self.background,(self.background_rect))
            self.all_defender.draw(self.screen)
            self.all_astroids.draw(self.screen)
            self.pygame.display.flip()

if __name__ == '__main__':                                
    settings = Settings()
    pygame.init()             
    game = Game(pygame, settings)
    game.run()
    pygame.quit()   