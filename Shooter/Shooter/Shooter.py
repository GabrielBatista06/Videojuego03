import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
def draw_text(surface, text, size, x, y):
 font = pygame.font.SysFont("serif", size)
 text_surface = font.render(text, True, WHITE)
 text_rect = text_surface.get_rect()
 text_rect.midtop = (x, y)
 surface.blit(text_surface, text_rect)
def draw_shield_bar(surface, x, y, percentage):
 BAR_LENGHT = 100
 BAR_HEIGHT = 10
 fill = (percentage / 100) * BAR_LENGHT
 border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
 fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
 pygame.draw.rect(surface, GREEN, fill)
 pygame.draw.rect(surface, WHITE, border, 2)
class Player(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load("assets/NAVE.png").convert()
  self.image.set_colorkey(BLACK)
  self.rect = self.image.get_rect()
  self.rect.centerx = WIDTH - 50
  self.rect.bottom = HEIGHT - 500
  self.speed_y = 0
  self.shield = 100
 def update(self):
  self.speed_y = 0
  keystate = pygame.key.get_pressed()
  if keystate[pygame.K_UP]:
   self.speed_y = -5
  if keystate[pygame.K_DOWN]:
   self.speed_y = 5
  self.rect.y += self.speed_y
  if self.rect.top < 0:
   self.rect.top = 0
  if self.rect.bottom > HEIGHT:
   self.rect.bottom = HEIGHT
 def shoot(self):
  bullet = Bullet(self.rect.centerx, self.rect.top)
  all_sprites.add(bullet)
  bullets.add(bullet)
  laser_sound.play()
class Meteor(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = random.choice(meteor_images)
  self.image.set_colorkey(BLACK)
  self.rect = self.image.get_rect()
  self.rect.x = random.randrange(550)
  self.rect.y = random.randrange(-600,0)
  self.speedy = random.randrange(1, 10)
 # self.speedx = random.randrange(-5, 5) #Los meteoritos se muevan en diversas direcciones
 def update(self):
  self.rect.y += self.speedy
  #self.rect.x += self.speedx
  if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
   self.rect.x = random.randrange(550)
   self.rect.y = random.randrange(-600,0)
   self.speedy = random.randrange(1, 10)
class Bullet(pygame.sprite.Sprite):
 def __init__(self, x, y):
  super().__init__()
  self.image = pygame.image.load("assets/LASER.png")
  self.image.set_colorkey(BLACK)
  self.rect = self.image.get_rect()
  self.rect.x = x-50
  self.rect.centery = y+55
  self.speedy = -10
 def update(self):
  self.rect.x += self.speedy
  if self.rect.bottom < 0:
   self.kill()
class Explosion(pygame.sprite.Sprite):
 def __init__(self, center):
  super().__init__()
  self.image = explosion_anim[0]
  self.rect = self.image.get_rect()
  self.rect.center = center
  self.frame = 0
  self.last_update = pygame.time.get_ticks()
  self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION
 def update(self):
  now = pygame.time.get_ticks()
  if now - self.last_update > self.frame_rate:
   self.last_update = now
   self.frame += 1
   if self.frame == len(explosion_anim):
    self.kill()
   else:
    center = self.rect.center
    self.image = explosion_anim[self.frame]
    self.rect = self.image.get_rect()
    self.rect.center = center
def show_go_screen():
 screen.blit(background1, [0,0])

 draw_text(screen, "Instruciones van aquí", 27, WIDTH // 2, HEIGHT // 2)
 draw_text(screen, "Press Key", 20, WIDTH // 2, HEIGHT * 3/4)
 pygame.display.flip()
 waiting = True
 while waiting:
  clock.tick(60)
  for event in pygame.event.get():
   if event.type == pygame.QUIT:
    pygame.quit()
   if event.type == pygame.KEYUP:
    waiting = False
meteor_images = []
meteor_list = ["assets/GLOBOC1.png", "assets/GLOBOB1.png","assets/GLOBOA1.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())
####----------------EXPLOSTION IMAGENES --------------
explosion_anim = []
for i in range(9):
 file = "assets/regularExplosion0{}.png".format(i)
 img = pygame.image.load(file).convert()
 img.set_colorkey(BLACK)
 img_scale = pygame.transform.scale(img, (70,70))
 explosion_anim.append(img_scale)
# Cargar imagen de fondo
background = pygame.image.load("assets/FONDO.png").convert()
background1 = pygame.image.load("assets/PATRÓN.png").convert()
# Cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)
#### ----------GAME OVER
game_over = True
running = True
while running:
 if game_over:
  show_go_screen()
  game_over = False
  all_sprites = pygame.sprite.Group()
  meteor_list = pygame.sprite.Group()
  bullets = pygame.sprite.Group()
  player = Player()
  all_sprites.add(player)
  for i in range(8):
   meteor = Meteor()
   all_sprites.add(meteor)
   meteor_list.add(meteor)
  score = 0
 clock.tick(60)
 for event in pygame.event.get():
  if event.type == pygame.QUIT:
   running = False
  elif event.type == pygame.KEYDOWN:
   if event.key == pygame.K_SPACE:
    player.shoot()
 all_sprites.update()
 #colisiones - meteoro - laser
 hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
 for hit in hits:
  score += 10
  #explosion_sound.play()
  explosion = Explosion(hit.rect.center)
  all_sprites.add(explosion)
  meteor = Meteor()
  all_sprites.add(meteor)
  meteor_list.add(meteor)
 # Checar colisiones - jugador - meteoro
 hits = pygame.sprite.spritecollide(player, meteor_list, True)
 for hit in hits:
  player.shield -= 25
  meteor = Meteor()
  all_sprites.add(meteor)
  meteor_list.add(meteor)
  if player.shield <= 0:
   game_over = True
 screen.blit(background, [0, 0])
 all_sprites.draw(screen)
 #Marcador
 draw_text(screen, str(score), 25, WIDTH // 2, 10)
 # Escudo.
 draw_shield_bar(screen, 5, 5, player.shield)
 pygame.display.flip()
pygame.quit()