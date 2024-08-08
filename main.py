import pygame, sys
import random
from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE,
                           KEYDOWN, QUIT)

pygame.init()
running = True
clock = pygame.time.Clock()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Player(pygame.sprite.Sprite):

  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.image.load("jet.png").convert()
    self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.surf.get_rect()

  def update(self, pressed_keys):
    if pressed_keys[K_UP]:
      self.rect.move_ip(0, -5)
    if pressed_keys[K_DOWN]:
      self.rect.move_ip(0, 5)
    if pressed_keys[K_LEFT]:
      self.rect.move_ip(-5, 0)
    if pressed_keys[K_RIGHT]:
      self.rect.move_ip(5, 0)

    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
      self.rect.right = SCREEN_WIDTH
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= SCREEN_HEIGHT:
      self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):

  def __init__(self):
    super(Enemy, self).__init__()
    self.surf = pygame.image.load("missile.png").convert()
    self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.surf.get_rect(center=(
        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
        random.randint(0, SCREEN_HEIGHT),
    ))
    self.speed = random.randint(1, 3)

    def update(self):
      self.rect.move_ip(-5, 0)
      if self.rect.right < 0:
        self.kill()

  def update(self):
    self.rect.move_ip(-self.speed, 0)
    if self.rect.right < 0:
      self.kill()


class Cloud(pygame.sprite.Sprite):

  def __init__(self):
    super(Cloud, self).__init__()
    self.surf = pygame.image.load("cloud.png").convert()
    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
    self.rect = self.surf.get_rect(center=(
        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
        random.randint(0, SCREEN_HEIGHT),
    ))

  def update(self):
    self.rect.move_ip(-5, 0)
    if self.rect.right < 0:
      self.kill()


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while running:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit
      print("Goodbye.")
      running = False
      sys.exit()
    elif event.type == ADDENEMY:
      new_enemy = Enemy()
      enemies.add(new_enemy)
      all_sprites.add(new_enemy)
    elif event.type == ADDCLOUD:
      new_cloud = Cloud()
      clouds.add(new_cloud)
      all_sprites.add(new_cloud)

  pressed_keys = pygame.key.get_pressed()
  player.update(pressed_keys)
  enemies.update()
  clouds.update()
  DISPLAYSURF.fill((135, 206, 250))
  for entity in all_sprites:
    DISPLAYSURF.blit(entity.surf, entity.rect)

  if pygame.sprite.spritecollideany(player, enemies):
    player.kill()
    running = False
  pygame.display.flip()
  clock.tick(30)
  pygame.display.update()
