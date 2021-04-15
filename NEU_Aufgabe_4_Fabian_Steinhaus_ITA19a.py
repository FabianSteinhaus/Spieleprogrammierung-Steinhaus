import pygame
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_DOWN)
import os
import random
import time
import sys

class Settings:
    window_width = 750
    window_height = 400
    fps = 60      
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    programStartTime = time.time()

    @staticmethod
    def get_dim():
        return (Settings.window_width, Settings.window_height)


class Background(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, filename)).convert()
        self.image = pygame.transform.scale(self.image, Settings.get_dim())
        self.background_rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.background_rect)


class Mouse(pygame.sprite.Sprite):
    def __init__(self,pygame):
        pygame.sprite.Sprite.__init__(self)
        self.pygame = pygame
        self.image = pygame.image.load(os.path.join(Settings.image_path, "heftzwecke5.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
    
    def update(self,screen):
        screen.blit(self.image, self.pygame.mouse.get_pos())
        self.rect = self.image.get_rect()


class Bubbles(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super().__init__()
        self.pygame = pygame
        self.imageOrig = pygame.image.load(os.path.join(Settings.image_path, "blase8.png")).convert_alpha()
        self.image = pygame.transform.scale(self.imageOrig, (5, 5))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.scale = 5
        self.time = time.time()
        self.random_position()
        self.possibleBubbles = 5

    def random_position(self):
        self.rect.left = random.randint(1, Settings.window_width)
        self.rect.top = random.randint(1, Settings.window_height)

    def scale_bubble(self):
        self.time_now = time.time()
        if (self.time_now - self.time) >= 1:
            self.time = time.time()
            self.scale = self.scale + random.randint(1, 4)
            self.image = self.pygame.transform.scale(self.imageOrig, (self.scale,self.scale))

    def draw(self, screen):
        pass

    def update(self, screen):
        self.screen = screen
        self.scale_bubble()


class Game:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.pygame = pygame
        self.pause = False
        self.screen = pygame.display.set_mode(Settings.get_dim())
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Steinhaus Aufgabe 4 Bubbles")
        self.background = Background("nature.jpg")
        self.background_rect = self.background.image.get_rect()
        self.all_Bubbles = pygame.sprite.Group()
        self.possibleBubbles = 3
        self.number_of_bubbles = 4
        self.time_next_birth = pygame.time.get_ticks()

        self.mouseCursor = Mouse(self.pygame)
        self.mouseGroup = pygame.sprite.Group()
        self.mouseGroup.add(self.mouseCursor)
        self.pygame.mouse.set_visible(False)
        self.old_time = time.time()

    def bubbleLimit(self):
        for x in range(1, self.possibleBubbles):
            self.timeNowLimit = time.time()
            if self.number_of_bubbles <= 18:
                if (self.timeNowLimit - self.old_time) >= 1: 
                    self.possibleBubbles = self.possibleBubbles + 1
                    self.old_time = time.time()
                    self.number_of_bubbles = self.number_of_bubbles + 1

    def createBubbles(self):
        self.bubbleLimit()
        if pygame.time.get_ticks() > self.time_next_birth:
            if self.all_Bubbles.__len__() <= self.possibleBubbles:         
                r = Bubbles(self.pygame)
                tries = 10
                while tries > 0:
                    if pygame.sprite.spritecollide(r, self.all_Bubbles, False):
                        tries = tries - 1
                    else:
                        self.all_Bubbles.add(r)

    def score(self):
        self.score_time = int(Settings.programStartTime)
        self.myfont = pygame.font.SysFont("monospace", 16)
        self.score_text = self.myfont.render("Punktestand = " + str(self.score_time), 1, (0,0,0))
        self.screen.blit(self.score_text, (20, 20))             # Hatte versucht einen Punktestand basierend auf die Zeit, die das Programm läuft, zu machen.
                                                                # Habe es aus Zeitgründen leider nicht mehr realisiert bekommen

    def show_pause(self):
            self.pauseImage = pygame.image.load(os.path.join(Settings.image_path, "Pausenbild2.png")).convert_alpha()
            self.pauseimageTransformed = pygame.transform.scale(self.pauseImage, (Settings.window_width, Settings.window_height))
            self.pauseimageTransformed.set_alpha(0)           
            self.all_Bubbles.draw(self.screen)
            self.screen.blit(self.pauseimageTransformed, self.background_rect)
   


    
    def watch_for_events(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    elif event.key == self.pygame.K_p:
                        self.pause = not self.pause


    def draw(self):
        if self.pause:
            self.show_pause()
        else:
            self.background.draw(self.screen)
            self.all_Bubbles.draw(self.screen)
            self.mouseGroup.update(self.screen)
        self.pygame.display.flip()

    def update(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.createBubbles()
            if not self.pause:
                self.all_Bubbles.update(self.screen)
            self.score()
            self.draw()
            
        pygame.quit()



if __name__ == '__main__':                                             
    game = Game()
    game.run()