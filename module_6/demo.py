import pygame
import random, sys, os, math, time
pygame.init()

# -----------------------
# Window / fonts / clock
# -----------------------
WIDTH, HEIGHT = 900, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival: City Escape")
clock = pygame.time.Clock()
FPS = 60

FONT = pygame.font.SysFont("Arial", 22)
BIG_FONT = pygame.font.SysFont("Arial", 46)

# -----------------------
# Colors
# -----------------------
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,30,30)
GREEN = (0,200,0)
YELLOW = (255,200,0)
GRAY = (40,40,40)
DARK_GRAY = (20,20,20)
HOVER = (255,140,0)
LOOT_COLOR_HEALTH = (120, 220, 180)
LOOT_COLOR_AMMO = (200, 200, 60)

# -----------------------
# Config / game state
# -----------------------
HIGHSCORE_FILE = "highscore.txt"

# Gameplay defaults (adjusted by difficulty)
player_speed = 4
zombie_base_speed = 1.6
spawn_delay_default = 1000 # ms

# Weapon definitions
weapon_list = ["pistol","shotgun","flamethrower"]
weapons = {
    "pistol": {"damage": 1, "ammo": 120, "color": (0,255,220), "rate": 220},
    "shotgun": {"damage": 3, "ammo": 40, "color": (255,200,0), "rate": 550},
    "flamethrower": {"damage": 5, "ammo": 20, "color": (255,100,0), "rate": 120}
}
current_weapon_index = 0
current_weapon = weapon_list[current_weapon_index]
last_shot_time = 0

# Game variables
score = 0
lives = 3
wave = 1
spawn_delay = spawn_delay_default
zombie_speed = zombie_base_speed
difficulty = "Normal"
volume = 60

# high scores list
if os.path.exists(HIGHSCORE_FILE):
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            data = f.read().strip()
            if data:
                high_scores = [int(x) for x in data.split(",") if x.strip().isdigit()]
            else:
                high_scores = []
    except Exception:
        high_scores = []
else:
    high_scores = []

# Game state machine
# Possible values: "menu", "settings", "highscore", "game", "gameover"
game_state = "menu"

# -----------------------
# Helper: load images safely (will fallback to colored surface)
# -----------------------
def load_image_safe(path, fallback_size=(40,40), fallback_color=(180,180,180)):
    try:
        img = pygame.image.load(path).convert_alpha()
        return img
    except Exception:
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf

# Try load images if in same folder (safe fallback if missing)
PLAYER_IMG = load_image_safe("./player.png", (48,48), (0,170,0))
ZOMBIE_IMG = load_image_safe("zombie.png", (48,48), (160,0,0))
# UPDATED: Increased fallback size for better visibility
LOOT_HEALTH_IMG = load_image_safe("loot_health.png", (30,30), LOOT_COLOR_HEALTH) 
LOOT_AMMO_IMG = load_image_safe("loot_ammo.png", (30,30), LOOT_COLOR_AMMO)
# UPDATED: Increased fallback size for better visibility
BULLET_IMG = load_image_safe("bullet.png", (10,6), (255,255,255))

# -----------------------
# Sprite classes (all update accept keys=None)
# -----------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = PLAYER_IMG
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = player_speed
        self.max_health = 10
        self.health = self.max_health
        # FIX: Invulnerability setup
        self.invulnerable_time = 1500 # 1.5 seconds of invulnerability
        self.last_hit_time = 0
        
    def update(self, keys=None):
        if keys is None:
            keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w]: dy -= self.speed
        if keys[pygame.K_s]: dy += self.speed
        if keys[pygame.K_a]: dx -= self.speed
        if keys[pygame.K_d]: dx += self.speed
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(WIN.get_rect())

        # FIX: Blink when invulnerable (visual feedback)
        now = pygame.time.get_ticks()
        if now - self.last_hit_time < self.invulnerable_time:
            # Simple blinking: show for 100ms, hide for 100ms
            if (now // 100) % 2 == 0:
                self.image = self.original_image
            else:
                self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        else:
            self.image = self.original_image

    def draw_health_bar(self, surf):
        w = max(32, self.rect.width)
        h = 6
        x = self.rect.centerx - w//2
        y = self.rect.top - 12
        pygame.draw.rect(surf, RED, (x,y,w,h))
        fill = int(w * (self.health/self.max_health))
        if fill>0:
            pygame.draw.rect(surf, GREEN, (x,y,fill,h))
            
    def take_damage(self, amount=1):
        global lives
        # FIX: Check invulnerability status
        now = pygame.time.get_ticks()
        if now - self.last_hit_time < self.invulnerable_time:
            return # Player is currently invulnerable
            
        # Damage applied
        self.health -= amount
        self.last_hit_time = now # Start invulnerability time
        
        if self.health <= 0:
            lives -= 1
            self.health = self.max_health
            if lives <= 0:
                set_state("gameover")

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=zombie_base_speed):
        super().__init__()
        self.original_image = ZOMBIE_IMG
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = speed
        self.max_health = 5
        self.health = self.max_health
    def update(self, keys=None):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, math.hypot(dx,dy))
        self.rect.x += int(self.speed * dx / dist)
        self.rect.y += int(self.speed * dy / dist)
    def draw_health_bar(self, surf):
        bar_w = max(24, self.rect.width)
        x = self.rect.centerx - bar_w//2
        y = self.rect.top - 8
        pygame.draw.rect(surf, RED, (x,y,bar_w,4))
        fill = int(bar_w * (self.health/self.max_health))
        if fill>0:
            pygame.draw.rect(surf, GREEN, (x,y,fill,4))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, color):
        super().__init__()
        
        self.image = BULLET_IMG.copy()
        
        # FIX: Check if the image is the small fallback, and fill with weapon color
        if self.image.get_width() <= 10 and self.image.get_height() <= 6:
            self.image.fill(color)
            
        self.rect = self.image.get_rect(center=pos)
        
        # FIX: Store position as float coordinates for smooth movement
        self.x = pos[0]
        self.y = pos[1]
        
        dx,dy = direction
        mag = max(1.0, math.hypot(dx,dy))
        self.vx = dx/mag * 13
        self.vy = dy/mag * 13
        
    def update(self, keys=None):
        # FIX: Update internal float position
        self.x += self.vx
        self.y += self.vy
        
        # FIX: Update the rect position using the rounded float position
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        
        # Check for boundary removal using float position
        if not WIN.get_rect().collidepoint(self.x, self.y):
            self.kill()

class Loot(pygame.sprite.Sprite):
    def __init__(self, pos, loot_type):
        super().__init__()
        self.type = loot_type
        if loot_type == "health":
            self.image = LOOT_HEALTH_IMG.copy()
        else:
            self.image = LOOT_AMMO_IMG.copy()
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
    def update(self, keys=None):
        # auto disappear after 20s
        if pygame.time.get_ticks() - self.spawn_time > 20000:
            self.kill()

# -----------------------
# Groups and player instance
# -----------------------
player = Player(WIDTH//2, HEIGHT//2)
players = pygame.sprite.GroupSingle(player)
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
loots = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

# -----------------------
# Utilities: highscore, state, difficulty, spawn, loot
# -----------------------
def load_highscores():
    global high_scores
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE,"r") as f:
                content = f.read().strip()
                if content:
                    high_scores = [int(x) for x in content.split(",") if x.strip().isdigit()]
                else:
                    high_scores = []
        except:
            high_scores = []
    else:
        high_scores = []

def save_highscores():
    try:
        with open(HIGHSCORE_FILE,"w") as f:
            f.write(",".join(str(x) for x in high_scores))
    except:
        pass

def add_highscore(val):
    high_scores.append(val)
    high_scores.sort(reverse=True)
    while len(high_scores) > 5:
        high_scores.pop()
    save_highscores()

def set_difficulty(level):
    global difficulty, zombie_speed, spawn_delay
    difficulty = level
    if level == "Easy":
        zombie_speed = 1.2
        spawn_delay = 1400
        player.speed = 5
    elif level == "Normal":
        zombie_speed = 1.8
        spawn_delay = 1000
        player.speed = 4
    elif level == "Hard":
        zombie_speed = 2.6
        spawn_delay = 700
        player.speed = 4

def set_state(s):
    global game_state
    game_state = s

def spawn_zombie_random():
    side = random.choice(["left","right","top","bottom"])
    if side=="left":
        x = -30; y = random.randint(0, HEIGHT)
    elif side=="right":
        x = WIDTH + 30; y = random.randint(0, HEIGHT)
    elif side=="top":
        x = random.randint(0, WIDTH); y = -30
    else:
        x = random.randint(0, WIDTH); y = HEIGHT + 30
    z = Zombie(x,y, speed = zombie_speed + (wave-1)*0.08)
    zombies.add(z); all_sprites.add(z)

def drop_loot_at(pos):
    if random.random() < 0.35:
        choice = random.choice(["health","ammo"])
        loot = Loot(pos, choice)
        loots.add(loot); all_sprites.add(loot)

def reset_game_vars():
    global score, lives, wave, current_weapon_index, current_weapon, last_shot_time
    score = 0
    lives = 3
    wave = 1
    current_weapon_index = 0
    current_weapon = weapon_list[current_weapon_index]
    last_shot_time = 0

def reset_game():
    global zombies, bullets, loots, all_sprites, player, players
    zombies.empty(); bullets.empty(); loots.empty()
    all_sprites.empty()
    player = Player(WIDTH//2, HEIGHT//2)
    players = pygame.sprite.GroupSingle(player)
    all_sprites.add(player)
    reset_game_vars()

# -----------------------
# UI Helpers
# -----------------------
def draw_text_center(surf, text, font, color, y):
    t = font.render(text, True, color)
    r = t.get_rect(center=(WIDTH//2, y))
    surf.blit(t, r)
    return r

def make_menu_buttons(options, start_y):
    buttons = []
    for i,opt in enumerate(options):
        surf = FONT.render(opt, True, WHITE)
        rect = surf.get_rect(center=(WIDTH//2, start_y + i*55))
        buttons.append((opt, surf, rect))
    return buttons

# -----------------------
# Menus & screens
# -----------------------
def main_menu_loop():
    global game_state
    options = ["Play Game", "Settings", "High Scores", "Quit"]
    buttons = make_menu_buttons(options, 300)
    while game_state == "menu":
        WIN.fill(DARK_GRAY)
        draw_text_center(WIN, "Zombie Survival: City Escape", BIG_FONT, YELLOW, 180)
        mx,my = pygame.mouse.get_pos()
        for opt, surf, rect in buttons:
            color = HOVER if rect.collidepoint(mx,my) else WHITE
            WIN.blit(FONT.render(opt, True, color), rect)
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for opt, surf, rect in buttons:
                    if rect.collidepoint(ev.pos):
                        if opt == "Play Game":
                            reset_game()
                            set_state("game")
                            return
                        elif opt == "Settings":
                            set_state("settings")
                            return
                        elif opt == "High Scores":
                            set_state("highscore")
                            return
                        elif opt == "Quit":
                            pygame.quit(); sys.exit()
        clock.tick(30)

def settings_loop():
    global difficulty, volume
    options = ["Difficulty: " + difficulty, "Volume: " + str(volume), "Back"]
    selected = 0
    diffs = ["Easy","Normal","Hard"]
    diff_idx = diffs.index(difficulty) if difficulty in diffs else 1
    while game_state == "settings":
        WIN.fill(GRAY)
        draw_text_center(WIN, "Settings", BIG_FONT, YELLOW, 140)
        mx,my = pygame.mouse.get_pos()
        for i,opt in enumerate(options):
            label = opt
            if i == 0:
                label = f"Difficulty: {difficulty}"
            elif i == 1:
                label = f"Volume: {volume}%"
            color = HOVER if i==selected else WHITE
            rect = FONT.render(label, True, color).get_rect(center=(WIDTH//2, 280 + i*50))
            WIN.blit(FONT.render(label, True, color), rect)
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    selected = (selected-1) % 3
                if ev.key == pygame.K_DOWN:
                    selected = (selected+1) % 3
                if ev.key == pygame.K_LEFT:
                    if selected == 0:
                        diff_idx = (diff_idx-1) % len(diffs)
                        set_difficulty(diffs[diff_idx])
                    elif selected == 1:
                        volume = max(0, volume-10)
                if ev.key == pygame.K_RIGHT:
                    if selected == 0:
                        diff_idx = (diff_idx+1) % len(diffs)
                        set_difficulty(diffs[diff_idx])
                    elif selected == 1:
                        volume = min(100, volume+10)
                if ev.key == pygame.K_RETURN and selected == 2:
                    set_state("menu")
                    return
                if ev.key == pygame.K_ESCAPE:
                    set_state("menu")
                    return
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # quick-click anywhere to return
                set_state("menu"); return
        clock.tick(30)

def highscore_loop():
    load_highscores()
    while game_state == "highscore":
        WIN.fill(DARK_GRAY)
        draw_text_center(WIN, "High Scores (Top 5)", BIG_FONT, YELLOW, 150)
        for i, val in enumerate(high_scores):
            draw_text_center(WIN, f"{i+1}. {val}", FONT, WHITE, 240 + i*36)
        draw_text_center(WIN, "Click or press ESC to return", FONT, WHITE, 520)
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                set_state("menu"); return
        clock.tick(30)

def gameover_loop():
    # called when state is gameover
    global score
    add_highscore(score)
    while game_state == "gameover":
        WIN.fill(BLACK)
        draw_text_center(WIN, "GAME OVER", BIG_FONT, RED, 200)
        draw_text_center(WIN, f"Score: {score}", FONT, WHITE, 270)
        draw_text_center(WIN, f"Highscore: {high_scores[0] if high_scores else 0}", FONT, YELLOW, 310)
        retry_surf = FONT.render("Retry", True, WHITE)
        menu_surf = FONT.render("Main Menu", True, WHITE)
        retry_rect = retry_surf.get_rect(center=(WIDTH//2 - 110, 420))
        menu_rect = menu_surf.get_rect(center=(WIDTH//2 + 110, 420))
        pygame.draw.rect(WIN, GRAY, retry_rect.inflate(18,10))
        pygame.draw.rect(WIN, GRAY, menu_rect.inflate(18,10))
        WIN.blit(retry_surf, retry_rect)
        WIN.blit(menu_surf, menu_rect)
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx,my = ev.pos
                if retry_rect.inflate(18,10).collidepoint(mx,my):
                    reset_game(); set_state("game"); return
                if menu_rect.inflate(18,10).collidepoint(mx,my):
                    reset_game(); set_state("menu"); return
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    reset_game(); set_state("game"); return
                if ev.key == pygame.K_m:
                    reset_game(); set_state("menu"); return
        clock.tick(30)

# -----------------------
# Main gameplay loop
# -----------------------
def game_loop():
    global last_shot_time, current_weapon, current_weapon_index, score, wave, spawn_delay
    spawn_timer = 0
    last_wave_time = pygame.time.get_ticks()
    wave_zombies_target = wave * 5

    while game_state == "game":
        dt = clock.tick(FPS)
        spawn_timer += dt
        WIN.fill((28,28,28))

        # ---------- events ----------
        keys = pygame.key.get_pressed()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEWHEEL:
                current_weapon_index = (current_weapon_index - ev.y) % len(weapon_list)
                current_weapon = weapon_list[current_weapon_index]
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    idx = int(ev.unicode)-1
                    if 0 <= idx < len(weapon_list):
                        current_weapon_index = idx
                        current_weapon = weapon_list[current_weapon_index]
                if ev.key == pygame.K_ESCAPE:
                    set_state("menu"); return

        mx,my = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # ---------- shooting ----------
        now = pygame.time.get_ticks()
        weapon_name = weapon_list[current_weapon_index]
        weapon_data = weapons[weapon_name]
        if mouse_pressed[0] and weapon_data["ammo"] > 0:
            if now - last_shot_time >= weapon_data["rate"]:
                dx = mx - player.rect.centerx
                dy = my - player.rect.centery
                # shotgun spreads
                if weapon_name == "shotgun":
                    pellets = 5
                    spread = 0.25
                    for i in range(pellets):
                        ang = math.atan2(dy, dx) + random.uniform(-spread, spread)
                        vx, vy = math.cos(ang), math.sin(ang)
                        b = Bullet(player.rect.center, (vx,vy), weapon_data["color"])
                        bullets.add(b); all_sprites.add(b)
                else:
                    b = Bullet(player.rect.center, (dx,dy), weapon_data["color"])
                    bullets.add(b); all_sprites.add(b)
                weapon_data["ammo"] -= 1
                last_shot_time = now

        # ---------- spawn zombies ----------
        if len(zombies) < wave_zombies_target and spawn_timer >= spawn_delay:
            spawn_zombie_random()
            spawn_timer = 0

        # ---------- updates (pass keys to update) ----------
        all_sprites.update(keys)

        # ---------- collisions: bullets -> zombies ----------
        for bullet in bullets:
            hit_z = pygame.sprite.spritecollide(bullet, zombies, False)
            if hit_z:
                for z in hit_z:
                    z.health -= weapons[weapon_list[current_weapon_index]]["damage"]
                    if z.health <= 0:
                        pos = z.rect.center
                        drop_loot_at(pos)
                        z.kill()
                        score += 10
                bullet.kill()

        # ---------- collisions: player <-> zombies ----------
        hitplayer = pygame.sprite.spritecollide(player, zombies, False)
        if hitplayer:
            # FIX: Damage applied using the new method with built-in cooldown
            player.take_damage(1)

        # ---------- collisions: player <-> loot ----------
        picked = pygame.sprite.spritecollide(player, loots, True)
        for it in picked:
            if it.type == "health":
                player.health = min(player.max_health, player.health + 4)
            elif it.type == "ammo":
                for w in weapons:
                    weapons[w]["ammo"] += 8

        # ---------- draw ----------
        all_sprites.draw(WIN)
        for z in zombies:
            z.draw_health_bar(WIN)
        player.draw_health_bar(WIN)

        # HUD
        score_surf = FONT.render(f"Score: {score}", True, WHITE)
        lives_surf = FONT.render(f"Lives: {lives}", True, WHITE)
        wave_surf = FONT.render(f"Wave: {wave}", True, WHITE)
        WIN.blit(score_surf, (WIDTH-210, 12))
        WIN.blit(lives_surf, (WIDTH-210, 36))
        WIN.blit(wave_surf, (WIDTH-210, 60))
        # weapon list & ammo
        y = 12
        for i,w in enumerate(weapon_list):
            color = YELLOW if i==current_weapon_index else WHITE
            ammo = weapons[w]["ammo"]
            txt = FONT.render(f"{i+1}. {w.capitalize()} ({ammo})", True, color)
            WIN.blit(txt, (10, y)); y += 26

        pygame.display.update()

        # ---------- wave progression ----------
        if len(zombies) == 0 and len(bullets) == 0:
            if pygame.time.get_ticks() - last_wave_time > 700:
                wave += 1
                wave_zombies_target = wave * 5
                last_wave_time = pygame.time.get_ticks()

# -----------------------
# Main program loop (state machine)
# -----------------------
def main():
    global game_state
    load_highscores()
    reset_game()
    set_difficulty(difficulty)
    while True:
        if game_state == "menu":
            main_menu_loop()
        elif game_state == "settings":
            settings_loop()
        elif game_state == "highscore":
            highscore_loop()
        elif game_state == "game":
            game_loop()
        elif game_state == "gameover":
            gameover_loop()
        else:
            set_state("menu")

if __name__ == "__main__":
    main()