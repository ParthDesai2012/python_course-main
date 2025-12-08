import pygame, random, sys, os

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival: City Escape")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
GRAY = (40, 40, 40)
DARK_GRAY = (20, 20, 20)
HOVER_COLOR = (255, 150, 0)
LOOT_COLOR = (0, 255, 255)

clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.SysFont("Arial", 26)
BIG_FONT = pygame.font.SysFont("Arial", 50)

# Game variables
player_speed = 5
zombie_speed = 2
spawn_delay = 1000
score = 0
lives = 5
difficulty = "Normal"
volume = 50
wave = 1

# High scores
HIGHSCORE_FILE = "highscore.txt"
if os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "r") as f:
        high_scores = [int(x) for x in f.read().split(",") if x.isdigit()]
else:
    high_scores = []

# Weapons
weapon_list = ["pistol", "shotgun", "flamethrower"]
weapons = {
    "pistol": {"damage": 1, "ammo": 100, "color": (0, 255, 255), "rate": 250},
    "shotgun": {"damage": 3, "ammo": 20, "color": (255, 200, 0), "rate": 600},
    "flamethrower": {"damage": 5, "ammo": 10, "color": (255, 100, 0), "rate": 100}
}
current_weapon_index = 0
current_weapon = weapon_list[current_weapon_index]
last_shot_time = 0

# Loot types
loot_types = ["health", "ammo"]
loot_items = pygame.sprite.Group()

# Game state
game_state = "menu"  # menu / settings / highscore / game / gameover

# Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("player.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        # Movement & health
        self.speed = 4
        self.health = 100
        self.max_health = 100

        # Shooting
        self.last_shot = 0
        self.shoot_delay = 300  # milliseconds

    def update(self, keys, dt):
        # Movement
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed

    def draw_health_bar(self, surface):
        bar_width = 40
        bar_height = 6
        fill = (self.health / self.max_health) * bar_width

        outline_rect = pygame.Rect(self.rect.centerx - bar_width//2, self.rect.top - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.centerx - bar_width//2, self.rect.top - 10, fill, bar_height)

        pygame.draw.rect(surface, (255, 0, 0), outline_rect)
        pygame.draw.rect(surface, (0, 255, 0), fill_rect)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.image.load("zombie.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.target = target
        self.speed = 1.2
        self.health = 50
        self.max_health = 50

    def update(self):
        dx = self.target.rect.x - self.rect.x
        dy = self.target.rect.y - self.rect.y
        dist = max(1, (dx*dx + dy*dy) ** 0.5)

        self.rect.x += (dx / dist) * self.speed
        self.rect.y += (dy / dist) * self.speed

    def draw_health_bar(self, surface):
        bar_width = 30
        bar_height = 5
        fill = (self.health / self.max_health) * bar_width

        outline = pygame.Rect(self.rect.centerx - bar_width//2, self.rect.top - 8, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.centerx - bar_width//2, self.rect.top - 8, fill, bar_height)

        pygame.draw.rect(surface, (255,0,0), outline)
        pygame.draw.rect(surface, (0,255,0), fill_rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,direction):
        super().__init__()
        self.image = pygame.Surface((10,5))
        self.image.fill(weapons[current_weapon]["color"])
        self.rect = self.image.get_rect(center=pos)
        self.dx,self.dy = direction
        self.vel = 10
    def update(self):
        self.rect.x += self.dx*self.vel
        self.rect.y += self.dy*self.vel
        if not WIN.get_rect().contains(self.rect):
            self.kill()

class Loot(pygame.sprite.Sprite):
    def __init__(self, pos, loot_type):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill(LOOT_COLOR if loot_type=="health" else YELLOW)
        self.rect = self.image.get_rect(center=pos)
        self.type = loot_type
    def update(self):
        if self.rect.colliderect(player.rect):
            if self.type=="health":
                player.health = min(player.max_health, player.health+5)
            elif self.type=="ammo":
                weapons[current_weapon]["ammo"] += 10
            self.kill()

player = Player()
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

# Utility functions
def draw_text_center(text,font,color,y):
    render = font.render(text,True,color)
    rect = render.get_rect(center=(WIDTH//2,y))
    WIN.blit(render,rect)

def spawn_zombie():
    z = Zombie()
    zombies.add(z)
    all_sprites.add(z)

def drop_loot(zombie):
    if random.random()<0.3:  # 30% chance
        loot_type = random.choice(loot_types)
        loot = Loot(zombie.rect.center, loot_type)
        loot_items.add(loot)
        all_sprites.add(loot)

def reset_game():
    global score,lives,zombies,bullets,all_sprites,player,wave
    score = 0
    lives = 5
    wave = 1
    zombies.empty()
    bullets.empty()
    loot_items.empty()
    all_sprites.empty()
    player = Player()
    all_sprites.add(player)

def save_highscore():
    global score, high_scores
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:5]
    with open(HIGHSCORE_FILE,"w") as f:
        f.write(",".join(map(str,high_scores)))

def set_difficulty(level):
    global difficulty,zombie_speed,spawn_delay
    difficulty = level
    if level=="Easy":
        zombie_speed,spawn_delay=1.5,1300
    elif level=="Normal":
        zombie_speed,spawn_delay=2.5,1000
    elif level=="Hard":
        zombie_speed,spawn_delay=3.5,700

def draw_hud():
    score_text = FONT.render(f"Score: {score}",True,WHITE)
    lives_text = FONT.render(f"Lives: {lives}",True,WHITE)
    wave_text = FONT.render(f"Wave: {wave}",True,WHITE)
    WIN.blit(score_text,(WIDTH-200,10))
    WIN.blit(lives_text,(WIDTH-200,40))
    WIN.blit(wave_text,(WIDTH-200,70))
    # Weapon inventory
    y=10
    for i,w in enumerate(weapon_list):
        color = YELLOW if i==current_weapon_index else WHITE
        ammo = weapons[w]["ammo"]
        label = f"{w.capitalize()} ({ammo})"
        WIN.blit(FONT.render(label,True,color),(10,y))
        y+=30

def menu_buttons(options,start_y):
    buttons=[]
    for i,opt in enumerate(options):
        text_surf = FONT.render(opt,True,WHITE)
        rect = text_surf.get_rect(center=(WIDTH//2,start_y+i*50))
        buttons.append((opt,rect))
    return buttons

def main_menu():
    global game_state
    options = ["Play Game","Settings","High Scores","Quit"]
    while True:
        WIN.fill(DARK_GRAY)
        draw_text_center("🧟 Zombie Survival 🧟",BIG_FONT,YELLOW,150)
        buttons = menu_buttons(options,300)
        mx,my = pygame.mouse.get_pos()
        for opt,rect in buttons:
            color = HOVER_COLOR if rect.collidepoint(mx,my) else WHITE
            WIN.blit(FONT.render(opt,True,color),rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                for opt,rect in buttons:
                    if rect.collidepoint(event.pos):
                        if opt=="Play Game":
                            game_state="game"
                            return
                        elif opt=="Settings":
                            game_state="settings"
                            return
                        elif opt=="High Scores":
                            game_state="highscore"
                            return
                        elif opt=="Quit":
                            pygame.quit()
                            sys.exit()
        clock.tick(30)

def settings_menu():
    global difficulty,volume,game_state
    options=["Difficulty","Volume","Back"]
    selected=0
    diffs=["Easy","Normal","Hard"]
    diff_idx = diffs.index(difficulty)
    while True:
        WIN.fill(GRAY)
        draw_text_center("Settings",BIG_FONT,YELLOW,150)
        mx,my = pygame.mouse.get_pos()
        for i,opt in enumerate(options):
            color = WHITE
            if opt=="Difficulty":
                label = f"{opt}: {difficulty}"
            elif opt=="Volume":
                label = f"{opt}: {volume}%"
            else:
                label = opt
            rect = FONT.render(label,True,color).get_rect(center=(WIDTH//2,300+i*50))
            WIN.blit(FONT.render(label,True,color),rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected=(selected-1)%len(options)
                elif event.key==pygame.K_DOWN:
                    selected=(selected+1)%len(options)
                elif event.key==pygame.K_LEFT:
                    if options[selected]=="Difficulty":
                        diff_idx = (diff_idx-1)%len(diffs)
                        set_difficulty(diffs[diff_idx])
                    elif options[selected]=="Volume":
                        volume=max(0,volume-10)
                elif event.key==pygame.K_RIGHT:
                    if options[selected]=="Difficulty":
                        diff_idx = (diff_idx+1)%len(diffs)
                        set_difficulty(diffs[diff_idx])
                    elif options[selected]=="Volume":
                        volume=min(100,volume+10)
                elif event.key==pygame.K_RETURN:
                    if options[selected]=="Back":
                        game_state="menu"
                        return
                elif event.key==pygame.K_ESCAPE:
                    game_state="menu"
                    return
        clock.tick(30)

def highscore_screen():
    global game_state
    while True:
        WIN.fill(DARK_GRAY)
        draw_text_center("High Scores",BIG_FONT,YELLOW,150)
        for i,s in enumerate(high_scores):
            draw_text_center(f"{i+1}. {s}",FONT,WHITE,250+i*40)
        draw_text_center("Click anywhere or ESC to return",FONT,WHITE,500)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN):
                game_state="menu"
                return

def game_over():
    global score, game_state
    save_highscore()
    while True:
        WIN.fill(BLACK)
        draw_text_center("GAME OVER!", BIG_FONT, RED, 220)
        draw_text_center(f"Score: {score}", FONT, WHITE, 290)
        draw_text_center(f"High Score: {high_scores[0] if high_scores else 0}", FONT, YELLOW, 330)

        # Draw buttons
        retry_text = FONT.render("Retry", True, WHITE)
        menu_text = FONT.render("Main Menu", True, WHITE)
        retry_rect = retry_text.get_rect(center=(WIDTH//2 - 120, 450))
        menu_rect = menu_text.get_rect(center=(WIDTH//2 + 120, 450))
        pygame.draw.rect(WIN, GRAY, retry_rect.inflate(20,10))
        pygame.draw.rect(WIN, GRAY, menu_rect.inflate(20,10))
        WIN.blit(retry_text, retry_rect)
        WIN.blit(menu_text, menu_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx,my = event.pos
                if retry_rect.inflate(20,10).collidepoint(mx,my):
                    reset_game()
                    game_state="game"
                    return
                elif menu_rect.inflate(20,10).collidepoint(mx,my):
                    reset_game()
                    game_state="menu"
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state="game"
                    return
                elif event.key == pygame.K_m:
                    reset_game()
                    game_state="menu"
                    return
        clock.tick(30)

def game_loop():
    global score,last_shot_time,current_weapon,current_weapon_index,wave,game_state
    spawn_timer=0
    wave_zombies = wave*5
    running=True
    while running and game_state=="game":
        dt = clock.tick(FPS)
        WIN.fill((30,30,30))
        mx,my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEWHEEL:
                current_weapon_index=(current_weapon_index-event.y)%len(weapon_list)
                current_weapon=weapon_list[current_weapon_index]
            if event.type==pygame.KEYDOWN:
                if event.key in (pygame.K_1,pygame.K_2,pygame.K_3):
                    current_weapon_index=int(event.unicode)-1
                    current_weapon=weapon_list[current_weapon_index]
                if event.key==pygame.K_ESCAPE:
                    game_state="menu"
                    return
        mouse_pressed=pygame.mouse.get_pressed()
        current_time=pygame.time.get_ticks()
        if mouse_pressed[0] and weapons[current_weapon]["ammo"]>0:
            if current_time-last_shot_time>=weapons[current_weapon]["rate"]:
                dx,dy = mx-player.rect.centerx, my-player.rect.centery
                dist=max(1,(dx**2+dy**2)**0.5)
                direction=(dx/dist,dy/dist)
                bullet=Bullet(player.rect.center,direction)
                bullets.add(bullet)
                all_sprites.add(bullet)
                weapons[current_weapon]["ammo"]-=1
                last_shot_time=current_time

        # Spawn zombies
        spawn_timer+=dt
        if len(zombies)<wave_zombies and spawn_timer>=spawn_delay:
            spawn_zombie()
            spawn_timer=0

        keys=pygame.key.get_pressed()
        player.update(keys)
        zombies.update()
        bullets.update()
        loot_items.update()

        # Bullet collision
        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet,zombies,False)
            for z in hits:
                z.health-=weapons[current_weapon]["damage"]
                if z.health<=0:
                    drop_loot(z)
                    z.kill()
                    score+=10
                bullet.kill()

        all_sprites.draw(WIN)
        for z in zombies:
            z.draw_health(WIN)
        player.draw_health(WIN)
        draw_hud()
        pygame.display.update()

        # Check wave completion
        if len(zombies)==0 and len(bullets)==0:
            wave += 1
            wave_zombies = wave*5
# Initialize game
reset_game()

while True:
    if game_state == "menu":
        main_menu()
    elif game_state == "settings":
        settings_menu()
    elif game_state == "highscore":
        highscore_screen()
    elif game_state == "game":
        game_loop()
    elif game_state == "gameover":
        game_over()
    else:
        game_state = "menu"  # fallback
