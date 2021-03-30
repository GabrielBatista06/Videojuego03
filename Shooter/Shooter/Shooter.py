import pygame, random



#Global values
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)
TEXT = (255, 255, 56)
SCORE=(240, 0, 0)
Counter = 0
Counter1=0
velocidad = 2
#Script start

pygame.init()

pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("ALIENS VS BALLOONS")

clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
 font = pygame.font.SysFont("arial", size)
 text_surface = font.render(text, True, TEXT)
 text_rect = text_surface.get_rect()
 text_rect.midtop = (x, y)
 surface.blit(text_surface, text_rect)

 #_________Grupo de BALLOONS___________#
def grupo():
 balloons = BALLOONS()
 all_sprites.add(balloons)
 balloons_list.add(balloons)

def draw_shield_bar(surface, x, y, percentage):
 BAR_LENGHT = 100
 BAR_HEIGHT = 10
 fill = (percentage / 100) * BAR_LENGHT
 border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
 fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
 pygame.draw.rect(surface, SCORE, fill)
 pygame.draw.rect(surface, WHITE, border, 2)

class Player(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load("./assets/NAVE.png").convert()
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
  if self.rect.bottom > HEIGHT:
   self.rect.bottom = HEIGHT
  if self.rect.top < 0:
   self.rect.top = 0

 def shoot(self):
  bullet = Bullet(self.rect.centerx, self.rect.top)
  all_sprites.add(bullet)
  bullets.add(bullet)
  laser_sound.play()

class BALLOONS(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = random.choice(balloons_images)
  self.image.set_colorkey(BLACK)
  self.rect = self.image.get_rect()
  self.rect.x = random.randrange(660)
  self.rect.y = random.randrange(-600,0)
  self.speedy = random.randrange(velocidad)

 def update(self):
  self.rect.y += self.speedy
  if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
   self.rect.x = random.randrange(660)
   self.rect.y = random.randrange(-600,0)
   self.speedy = random.randrange(velocidad)

class Bullet(pygame.sprite.Sprite):
 def __init__(self, x, y):
  super().__init__()
  self.image = pygame.image.load("./assets/LASER.png")
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
 draw_text(screen, "↑ up and ↓ down to move / backspace to shoot", 30, WIDTH // 2, HEIGHT // 2.90)
 draw_text(screen, "Press any Key", 22, WIDTH // 2, HEIGHT * 3/4)
 pygame.display.flip()
 waiting = True
 while waiting:
  clock.tick(60)
  for event in pygame.event.get():
   if event.type == pygame.QUIT:
    pygame.quit()
   if event.type == pygame.KEYUP:
    waiting = False
balloons_images = []
balloons_list = ["./assets/GLOBOC1.png", "./assets/GLOBOB1.png","./assets/GLOBOA1.png"]
for img in balloons_list:
    balloons_images.append(pygame.image.load(img).convert())
####----------------EXPLOSTION IMAGENES --------------
explosion_anim = []
for i in range(3):
 file = "./assets/regularExplosion0{}.png".format(i)
 img = pygame.image.load(file).convert()
 img.set_colorkey(BLACK)
 img_scale = pygame.transform.scale(img, (70,70))
 explosion_anim.append(img_scale)
# Cargar imagen de fondo
background = pygame.image.load("./assets/FONDO.png").convert()
background1 = pygame.image.load("./assets/PATRON.png").convert()
background1.set_colorkey(BLACK)
# Cargar sonidos
laser_sound = pygame.mixer.Sound("./assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("./assets/Explosion.mp3")
pygame.mixer.music.load("./assets/music.ogg")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)
#### ----------GAME OVER
game_over = True
running = True
#----------BUCLE PRINCIPAL------------#
Player.shield = 100
while running:
#----Implementacion del tiempo---------#
 Counter += 1
 Counter1 +=1 
 if Counter == 100:
    player.shield -= 20
    Counter = 0
    if player.shield <= 0:
      velocidad=3
      game_over = True
 if Counter1 == 100:
    velocidad +=1
    Counter1=0

 if game_over:  
  show_go_screen()
  game_over = False

  all_sprites = pygame.sprite.Group()
  balloons_list = pygame.sprite.Group()
  bullets = pygame.sprite.Group()
  player = Player()
  all_sprites.add(player)
  for i in range(5):
    grupo()
  score = 0
 clock.tick(60)
 for event in pygame.event.get():
  if event.type == pygame.QUIT:
   running = False
  elif event.type == pygame.KEYDOWN:
   if event.key == pygame.K_SPACE:
    player.shoot()
 all_sprites.update()
 #colisiones - balloons - laser
 hits = pygame.sprite.groupcollide(balloons_list, bullets, True, True)
 for hit in hits:
  score += 10
  explosion_sound.play()
  explosion = Explosion(hit.rect.center)
  all_sprites.add(explosion)
  grupo()
 # Checar colisiones - jugador - balloons
  Colision = pygame.sprite.groupcollide(balloons_list, bullets, True, True)
  if Colision == pygame.sprite.groupcollide(balloons_list, bullets, False,False)  and player.shield < 100: 
    player.shield+=10
    grupo()
  
 screen.blit(background, [0, 0])
 all_sprites.draw(screen)
 #Marcador
 draw_text(screen, str(score), 25, WIDTH // 2, 10)
 # Escudo.
 draw_shield_bar(screen, 5, 5, player.shield)
 pygame.display.flip()

pygame.quit()