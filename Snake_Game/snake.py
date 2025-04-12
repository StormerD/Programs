import pygame, sys, random
from pygame.math import Vector2

# - - - CLASS - - -
class SNAKE:
  def __init__(self):
    self.Body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
    self.Direction = Vector2(1, 0)
    self.NewBlock = False
    
  def Draw(self):
    for _block in self.Body:
      xPos = int(_block.x * _cellSize)
      yPos = int(_block.y * _cellSize)
      _snakeBlock = pygame.Rect(xPos, yPos, _cellSize, _cellSize)
      pygame.draw.rect(screen, (0, 255, 0), _snakeBlock)
      
  def Move(self):
    if self.NewBlock == True:
      _bodyCopy = self.Body[:]
    else:
      _bodyCopy = self.Body[:-1]
    _bodyCopy.insert(00, _bodyCopy[0] + self.Direction)
    self.Body = _bodyCopy[:]
    self.NewBlock = False
    
  def AddBlock(self):
    self.NewBlock = True

# - - - CLASS - - -
class FRUIT:
  def __init__(self):
   self.NewPos()
    
  def Draw(self):
    _fruitRect = pygame.Rect(int(self.Pos.x) * _cellSize, int(self.Pos.y) * _cellSize, _cellSize, _cellSize)
    pygame.draw.rect(screen, (126, 0, 64), _fruitRect)
    
  def NewPos(self):
    self.x = random.randint(0, _cellNumber - 1)
    self.y = random.randint(0, _cellNumber - 1)
    self.Pos = Vector2(self.x, self.y)

# - - - CLASS - - -
class MAIN:
  def __init__(self):
    self.Snake = SNAKE()
    self.Fruit = FRUIT()
    self.CanInput = True
    
  def Update(self):
    self.Snake.Move()
    self.DetectCollision()
    self.DetectFail()
    self.CanInput = True
  
  def DrawElements(self):
    self.Fruit.Draw()
    self.Snake.Draw()
    
  def DetectCollision(self):
    if self.Fruit.Pos == self.Snake.Body[0]:
      self.Fruit.NewPos()
      self.Snake.AddBlock()
  
  def DetectFail(self):
    if not 0 <= self.Snake.Body[0].x <= _cellNumber - 1 or not 0 <= self.Snake.Body[0].y <= _cellNumber - 1:
      self.GameOver()
    for _block in self.Snake.Body[1:]:
      if _block == self.Snake.Body[0]:
        self.GameOver()

  def GameOver(self):
    pygame.quit()
    sys.exit()

# - - - GAME INIT - - -
pygame.init()
_cellSize = 40
_cellNumber = 20
screen = pygame.display.set_mode((_cellNumber * _cellSize, _cellNumber * _cellSize))
clock = pygame.time.Clock()

MainGame = MAIN()

# - - - GAME EVENTS - - -
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# - - - GAME LOOP - - -
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == SCREEN_UPDATE:
      MainGame.Update()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        if MainGame.Snake.Direction.x != 1 and MainGame.CanInput == True:
          MainGame.Snake.Direction = Vector2(-1, 0)
          MainGame.CanInput = False
      if event.key == pygame.K_DOWN:
        if MainGame.Snake.Direction.y != -1 and MainGame.CanInput == True:
          MainGame.Snake.Direction = Vector2(0, 1)
          MainGame.CanInput = False
      if event.key == pygame.K_RIGHT:
        if MainGame.Snake.Direction.x != -1 and MainGame.CanInput == True:
          MainGame.Snake.Direction = Vector2(1, 0)
          MainGame.CanInput = False
      if event.key == pygame.K_UP:
        if MainGame.Snake.Direction.y != 1 and MainGame.CanInput == True:
          MainGame.Snake.Direction = Vector2(0, -1)
          MainGame.CanInput = False
      
  screen.fill((175, 215, 70))
  MainGame.DrawElements()

# - - - GAME LOOP UPDATE - - -
  pygame.display.update()
  clock.tick(60)