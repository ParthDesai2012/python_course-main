import pygame
import random
from zombie import Zombie

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival: City Escape")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 5
        self.health = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed
        # Keep inside screen
        self.rect.clamp_ip(screen.get_rect())

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        dx, dy = target_pos[0]-x, target_pos[1]-y
        distance = max((dx**2 + dy**2)**0.5, 1)
        self.velocity = (dx/distance*10, dy/distance*10)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # Remove if out of screen
        if not screen.get_rect().collidepoint(self.rect.center):
            self.kill()

# Sprite groups
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

zombie_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# Spawn some zombies
for _ in range(5):
    x = random.choice([random.randint(-100, -40), random.randint(WIDTH+40, WIDTH+100)])
    y = random.choice([random.randint(-100, -40), random.randint(HEIGHT+40, HEIGHT+100)])
    zombie = Zombie(x, y)
    zombie_group.add(zombie)

# Score
score = 0

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Shoot bullet
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            bullet = Bullet(player.rect.centerx, player.rect.centery, mouse_pos)
            bullet_group.add(bullet)

    # Update
    player_group.update()
    bullet_group.update()
    zombie_group.update(player)

    # Bullet-Zombie collision
    for bullet in bullet_group:
        hit_zombies = pygame.sprite.spritecollide(bullet, zombie_group, False)
        for zombie in hit_zombies:
            zombie.take_damage(25)
            bullet.kill()
            if not zombie.alive():
                score += 10

    # Zombie-Player collision
    hits = pygame.sprite.spritecollide(player, zombie_group, False)
    for zombie in hits:
        player.health -= 1
        if player.health <= 0:
            running = False
            print("Game Over! Final Score:", score)

    # Draw
    screen.fill((30,30,30))
    player_group.draw(screen)
    bullet_group.draw(screen)
    zombie_group.draw(screen)

    # HUD
    pygame.draw.rect(screen, RED, (10, 10, 100, 10))
    pygame.draw.rect(screen, GREEN, (10, 10, player.health, 10))
    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 30))

    pygame.display.flip()

pygame.quit()
