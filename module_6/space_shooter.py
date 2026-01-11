import pygame
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Background image
background = pygame.image.load("space_bg.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Background music
pygame.mixer.music.load("space_music.mp3")
pygame.mixer.music.play(-1)   # Loop forever

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load('space_shooter(player).png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 40))
            print("✓ Player sprite loaded!")
        except Exception as e:
            print(f"✗ Could not load space_shooter(player).png: {e}")
            self.image = pygame.Surface((50, 40))
            self.image.fill(BLUE)
            pygame.draw.polygon(self.image, WHITE, [(25, 0), (0, 40), (50, 40)])

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.health = 100
        self.shoot_delay = 100
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullet = Bullet(self.rect.centerx, self.rect.top, mouse_x, mouse_y)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load('space_shooter(enemy).png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 30))
            print("✓ Enemy sprite loaded!")
        except Exception as e:
            print(f"✗ Could not load space_shooter(enemy).png: {e}")
            self.image = pygame.Surface((40, 30))
            self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        try:
            self.image = pygame.image.load('space_shooter(bullet).png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (10, 20))
            print("✓ Bullet sprite loaded!")
        except Exception as e:
            print(f"✗ Could not load space_shooter(bullet).png: {e}")
            self.image = pygame.Surface((5, 15))
            self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance != 0:
            self.speedx = (dx / distance) * 15
            self.speedy = (dy / distance) * 15
        else:
            self.speedx = 0
            self.speedy = -15

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or 
            self.rect.right < 0 or self.rect.left > WIDTH):
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        for i in range(5):
            img = pygame.Surface((40 + i*10, 40 + i*10))
            img.fill(BLACK)
            img.set_colorkey(BLACK)
            pygame.draw.circle(img, YELLOW, (20 + i*5, 20 + i*5), 20 + i*5)
            pygame.draw.circle(img, RED, (20 + i*5, 20 + i*5), 15 + i*3)
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index == len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game variables
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
game_over = False

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                game_over = False
                score = 0
                player.health = 100
                all_sprites.empty()
                enemies.empty()
                bullets.empty()
                player = Player()
                all_sprites.add(player)
                for i in range(8):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)

    if not game_over:
        all_sprites.update()

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            player.health -= 20
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            if player.health <= 0:
                game_over = True

    # Draw
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.draw.rect(screen, RED, (10, 50, 200, 20))
    pygame.draw.rect(screen, GREEN, (10, 50, max(0, player.health * 2), 20))
    health_text = font.render(f"Health: {max(0, player.health)}", True, WHITE)
    screen.blit(health_text, (10, 75))
    
    if game_over:
        game_over_text = font.render("GAME OVER!", True, RED)
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 20))
        screen.blit(restart_text, (WIDTH//2 - 150, HEIGHT//2 + 20))
    
    pygame.display.flip()

pygame.quit()
