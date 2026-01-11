import pygame
import random
import math
import os

# ==========================
# FILE PATH SETUP
# ==========================

BASE_PATH = r"C:\Users\PDgamerPRO\OneDrive\Desktop\python_course-main"

BG_PATH = os.path.join(BASE_PATH, "space_bg.png")
MUSIC_PATH = os.path.join(BASE_PATH, "space_music.mp3")
PLAYER_PATH = os.path.join(BASE_PATH, "space_shooter(player).png")
ENEMY_PATH = os.path.join(BASE_PATH, "space_shooter(enemy).png")
BULLET_PATH = os.path.join(BASE_PATH, "space_shooter(bullet).png")

# ==========================
# INITIALIZE
# ==========================

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# ==========================
# LOAD BACKGROUND
# ==========================

try:
    background = pygame.image.load(BG_PATH).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    print("✓ Background loaded")
except:
    print("✗ Background not found – using black screen")
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((0, 0, 0))

# ==========================
# LOAD MUSIC
# ==========================

try:
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.play(-1)
    print("✓ Music loaded")
except:
    print("✗ Music file not found – silent mode activated")

# ==========================
# COLORS
# ==========================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
FPS = 60

# ==========================
# PLAYER CLASS
# ==========================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(PLAYER_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 40))
            print("✓ Player sprite loaded")
        except:
            print("✗ Player sprite missing – using fallback")
            self.image = pygame.Surface((50, 40))
            self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.health = 100
        self.shoot_delay = 150
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        if pygame.mouse.get_pressed()[0]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            mx, my = pygame.mouse.get_pos()
            bullet = Bullet(self.rect.centerx, self.rect.top, mx, my)
            all_sprites.add(bullet)
            bullets.add(bullet)

# ==========================
# ENEMY CLASS
# ==========================

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(ENEMY_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 30))
            print("✓ Enemy sprite loaded")
        except:
            print("✗ Enemy sprite missing – using fallback")
            self.image = pygame.Surface((40, 30))
            self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > HEIGHT + 10:
            self.rect.y = random.randrange(-100, -40)
            self.rect.x = random.randrange(WIDTH - self.rect.width)

# ==========================
# BULLET CLASS
# ==========================

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, tx, ty):
        super().__init__()
        try:
            self.image = pygame.image.load(BULLET_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, (10, 20))
            print("✓ Bullet sprite loaded")
        except:
            print("✗ Bullet sprite missing – using fallback")
            self.image = pygame.Surface((5, 15))
            self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        dx = tx - x
        dy = ty - y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist == 0:
            dist = 1

        self.speedx = dx / dist * 15
        self.speedy = dy / dist * 15

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# ==========================
# SPRITES
# ==========================

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(7):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

font = pygame.font.Font(None, 36)
score = 0

# ==========================
# GAME LOOP
# ==========================

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Bullet hits enemy
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Enemy hits player
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.health -= 20
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f"Health: {player.health}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 40))

    pygame.display.flip()

pygame.quit()
