import pygame as pg
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_DOWN)
from dataclasses import dataclass
import random
import os
import time
import sys

pg.init()

pg.display.set_caption("Fabian Steinhaus Auftrag 5: Minesweeper")                           # Programm Beschriftung wird erstellt

class Settings:
      fps = 20
      screen_size = 800
      grid_size = 20
      possible_mines = 50
      cell_size = screen_size // grid_size 
      clock = pg.time.Clock()

      @staticmethod
      def get_dim():
          return (Settings.screen_size, Settings.screen_size)

 

class Designer:
    font = pg.font.Font(None, 35)
    font_color = pg.Color('red')
    passed_time = 0
    timer_started = True
    start_time = pg.time.get_ticks()


def load_bitmap(filename):                                                                  # Methode zum Laden und skalieren von Bildern
      file_path = os.path.dirname(os.path.abspath(__file__))
      image_path = os.path.join(file_path, "images")
      image = pg.image.load(os.path.join(image_path, filename)).convert()
      return pg.transform.scale(image, (Settings.cell_size, Settings.cell_size))

screen = pg.display.set_mode(Settings.get_dim())                                            # Bildschirm-Variable wird erstellt


bitmap_normal = load_bitmap('Minesweeper_normal.png')
bitmap_mine = load_bitmap('Minesweeper_mine.png')
bitmap_flagged = load_bitmap('Minesweeper_flag.png')



cell_picture = []                                                                           # Neun Bilder werden einer Liste hinzugefügt
for n in range(9):
  cell_picture.append(load_bitmap(f'Minesweeper_{n}.png'))


matrix = []
cells_nearby =  [(-1, -1),  (0, -1),  (1, -1),                                               # Liste mit den benachbarten Feldern einer Zelle
                 (-1, -0),            (1, 0),
                 (-1, 1),   (0, 1),   (1, 1)]


def valid(y, x):                                                                             # Methode zum überprüfen der Gültigkeit
      return y > -1 and y < Settings.grid_size and x > -1 and x < Settings.grid_size


@dataclass
class Cell():
  line: int
  column: int
  mine = False
  reveal = False
  flagged = False
  number_of_mines = 0
  total_mines = Settings.possible_mines


  def show(self):                                                                   
    x_y = (self.column * Settings.cell_size, self.line * Settings.cell_size)                # Methode zum blitten der Bilder
    if self.reveal:
      if self.mine:
        screen.blit(bitmap_mine, x_y)
      else:
        screen.blit(cell_picture[self.number_of_mines], x_y)
    else:
      if self.flagged:
        screen.blit(bitmap_flagged, x_y)
      else:
        screen.blit(bitmap_normal, x_y)


  def get_number_of_mines(self):                                                            # Methode, die die Anzahl an Minen in der nähe eines Feldes erfasst
    for x_y in cells_nearby:
      new_line = self.line + x_y[0]
      new_column = self.column + x_y[1]
      if valid(new_line, new_column) and matrix[new_line * Settings.grid_size+new_column].mine:
        self.number_of_mines = self.number_of_mines + 1


def fill_free_next(line, column):                                                           # Methode zum offen legen von mehreren leeren Feldern
  for x_y in cells_nearby:
    new_line = line + x_y[0]
    new_column = column + x_y[1]
    if valid(new_line, new_column):
      cell = matrix[new_line*Settings.grid_size+new_column]
      if cell.number_of_mines == 0 and not cell.reveal: 
        cell.reveal = True
        fill_free_next(new_line, new_column)
      else:
        cell.reveal = True


for n in range(Settings.grid_size * Settings.grid_size):                                    # Schleife zum Hinzufügen der Objekte in das Raster
  matrix.append(Cell(n // Settings.grid_size, n % Settings.grid_size))


while Settings.possible_mines > 0:                                                          # Schleife zum zufälligen Verteilen der Minen
  cell = matrix[random.randrange(Settings.grid_size*Settings.grid_size)]
  if not cell.mine:
    cell.mine = True
    Settings.possible_mines = Settings.possible_mines - 1


for objekt in matrix:           
    if not objekt.mine:
        objekt.get_number_of_mines()


def watch_for_other_events():                                                               # Methode zum erfassen von Events 
    if event.type == pg.MOUSEBUTTONDOWN:
                  mouseX, mouseY = pg.mouse.get_pos()
                  cell_mouse_y = mouseY // Settings.cell_size 
                  cell_mouse_x = mouseX // Settings.cell_size
                  cell = matrix[cell_mouse_y * Settings.grid_size + cell_mouse_x]

                  if pg.mouse.get_pressed()[2]:
                        cell.flagged = not cell.flagged
                        Cell.total_mines = Cell.total_mines -1
                  if pg.mouse.get_pressed()[0]:
                        cell.reveal = True
                              
                        if cell.number_of_mines == 0 and not cell.mine:
                              fill_free_next(cell_mouse_y, cell_mouse_x)
                        if cell.mine:
                            for objekt in matrix:
                                objekt.reveal = True 
                        

def draw():                                                                                 # Methode zum Blitten von allem
    for objekt in matrix: 
        objekt.show()
    screen.blit(timer_text, (Settings.screen_size - 50, 15))
    screen.blit(bomb_text, (20, 15))
    pg.display.flip()
    

run = True

while run:                                                                                  # Hauptprogrammschleife
  Settings.clock.tick(Settings.fps)
  passed_time = pg.time.get_ticks() - Designer.start_time
  timer_text = Designer.font.render(str(int(passed_time / 1000)), True, Designer.font_color)
  bomb_text = Designer.font.render(str(Cell.total_mines), True, Designer.font_color)

  for event in pg.event.get():
      if event.type == QUIT:
            run = False 
      elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False
                    elif event.key == pg.K_q:
                        run = False
      watch_for_other_events()
  draw()

pg.quit()