import pygame, sys
from pygame.math import Vector2

class Fruit:
  def __init__(self):
    self.X = 5
    self.Y = 4
    self.Pos = Vector2(self.X, self.Y)
    
  def DrawFruit(self):
    _fruitRect = pygame.Rect(self.Pos.X, self.Pos.Y, _cellSize, _cellSize)
    pygame.draw.rect(screen(126, 166, 144), _fruitRect)

pygame.init()
_cellSize = 40
_cellNumber = 20
screen = pygame.display.set_mode((_cellNumber * _cellSize, _cellNumber * _cellSize))
clock = pygame.time.Clock()

_fruit = Fruit()

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
      
  screen.fill((175, 215, 70))
  _fruit.DrawFruit()

  pygame.display.update()
  clock.tick(60)