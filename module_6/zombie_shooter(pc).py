# zombie_final.py
# Dual PC + Mobile version (auto-detect). Joystick only on mobile.
# Required/optional assets in same folder:
# player.png, zombie.png, fireball.jpeg, main_menu.png, bg.png
# Fallback shapes used if images missing.

import pygame, sys, os, random, math, time
pygame.init()

# -------- window / fonts / clock --------
WIDTH, HEIGHT = 900, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival: City Escape")
CLOCK = pygame.time.Clock()
FPS = 60

FONT = pygame.font.SysFont("Arial", 20)
BIG_FONT = pygame.font.SysFont("Arial", 36)
SMALL_FONT = pygame.font.SysFont("Arial", 14)

# -------- colors & defaults --------
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,30,30)
GREEN = (0,200,0)
YELLOW = (255,200,0)
GRAY = (140,140,140)
ACCENT = (70,160,255)

# -------- gameplay defaults --------
PLAYER_SPEED = 4
ZOMBIE_BASE_SPEED = 1.6
SPAWN_DELAY = 900  # ms between spawns in a wave

WEAPON_LIST = ["pistol","shotgun","flamethrower"]
WEAPONS = {
    "pistol": {"damage": 12, "ammo": 999, "rate": 220},
    "shotgun": {"damage": 18, "ammo": 60, "rate": 600},
    "flamethrower": {"damage": 8, "ammo": 200, "rate": 80}
}

HIGHSCORE_FILE = "highscore.txt"

# -------- robust image loader --------
def load_image_safe(name, size=None, fallback_color=(180,180,180)):
    path = os.path.join(os.getcwd(), name)
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except Exception:
        if size is None:
            size = (40,40)
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf

# load assets (only those you told me you have; others fallback)
PLAYER_R = load_image_safe("player.png", (48,48), (0,160,0))
PLAYER_L = load_image_safe("player-left.png", (48,48), (0,120,0))  # optional
ZOMBIE_SRC = load_image_safe("zombie.png", (48,48), (160,0,0))
ZOMBIE_IMG = pygame.transform.smoothscale(ZOMBIE_SRC, (36,36))
FIRE_IMG = load_image_safe("fireball.jpeg", (28,28), (255,80,0))
BG_IMG = load_image_safe("bg.png", (WIDTH,HEIGHT), (40,40,80))
MENU_BG = load_image_safe("main_menu.png", (WIDTH,HEIGHT), (25,25,25))

# bullet shapes for pistol / shotgun
def make_circle(col, d):
    s = pygame.Surface((d,d), pygame.SRCALPHA)
    pygame.draw.circle(s, col, (d//2,d//2), d//2)
    return s
PISTOL_BULLET = make_circle((255,140,0), 10)
SHOTGUN_BULLET = make_circle((255,220,0), 8)

# -------- UI helpers --------
def rounded_rect(surface, rect, color, radius=10):
    x,y,w,h = rect
    r = radius
    pygame.draw.rect(surface, color, (x+r, y, w-2*r, h))
    pygame.draw.rect(surface, color, (x, y+r, w, h-2*r))
    pygame.draw.circle(surface, color, (x+r, y+r), r)
    pygame.draw.circle(surface, color, (x+w-r, y+r), r)
    pygame.draw.circle(surface, color, (x+r, y+h-r), r)
    pygame.draw.circle(surface, color, (x+w-r, y+h-r), r)

def draw_button(surface, rect, text, mouse_pos, click_pos):
    hovered = rect.collidepoint(mouse_pos)
    rounded_rect(surface, (rect.x, rect.y, rect.w, rect.h), (35,35,35), 12)
    border_color = ACCENT if hovered else (200,200,200)
    pygame.draw.rect(surface, border_color, rect, 2, border_radius=12)
    color = WHITE if hovered else (220,220,220)
    txt = FONT.render(text, True, color)
    surface.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
    return (click_pos is not None and rect.collidepoint(click_pos))

def draw_text_center(surface, text, font, color, y):
    surf = font.render(text, True, color)
    r = surf.get_rect(center=(WIDTH//2, y))
    surface.blit(surf, r)
    return r

# -------- Sprites --------
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img_r = PLAYER_R
        self.img_l = PLAYER_L
        self.facing_right = True
        self.image = self.img_r.copy()
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = PLAYER_SPEED
        self.max_health = 100
        self.health = self.max_health
        self.weapon_index = 0
        self.weapon = WEAPON_LIST[self.weapon_index]
        self.last_shot = 0
        self.bob = 0
        self.bob_dir = 1

    def update(self, keys=None, mobile_input=None):
        if keys is None and mobile_input is None:
            keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys is not None:
            if keys[pygame.K_w]: dy -= self.speed
            if keys[pygame.K_s]: dy += self.speed
            if keys[pygame.K_a]:
                dx -= self.speed; self.facing_right = False
            if keys[pygame.K_d]:
                dx += self.speed; self.facing_right = True
        if mobile_input:
            if mobile_input.get("left"): dx -= self.speed
            if mobile_input.get("right"): dx += self.speed
            if mobile_input.get("left"): self.facing_right = False
            if mobile_input.get("right"): self.facing_right = True

        self.rect.x += dx; self.rect.y += dy
        self.rect.clamp_ip(WIN.get_rect())

        # bob animation
        self.bob += 0.15 * self.bob_dir
        if abs(self.bob) > 2: self.bob_dir *= -1

        self.image = self.img_r if self.facing_right else self.img_l

    def switch_weapon(self, idx):
        if 0 <= idx < len(WEAPON_LIST):
            self.weapon_index = idx
            self.weapon = WEAPON_LIST[idx]

    def switch_weapon_scroll(self, d):
        self.weapon_index = (self.weapon_index + d) % len(WEAPON_LIST)
        self.weapon = WEAPON_LIST[self.weapon_index]

    def draw_health(self, surf):
        w,h = 44,7
        x = self.rect.centerx - w//2; y = self.rect.top - 12
        pygame.draw.rect(surf, RED, (x,y,w,h))
        fill = int(w * (self.health/self.max_health))
        if fill>0: pygame.draw.rect(surf, GREEN, (x,y,fill,h))

    def take_damage(self, amt):
        global lives, game_state
        self.health -= amt
        if self.health <= 0:
            lives -= 1
            self.health = self.max_health
            if lives <= 0:
                set_state("gameover")

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, is_boss=False):
        super().__init__()
        self.base = ZOMBIE_IMG
        self.image = self.base.copy()
        self.rect = self.image.get_rect(center=(x,y))
        self.is_boss = is_boss
        self.speed = ZOMBIE_BASE_SPEED + random.uniform(-0.2,0.6)
        self.max_health = 140 if is_boss else 40
        self.health = self.max_health + (20*(wave-1) if is_boss else 0)
        self.hurt_timer = 0

    def update(self, target=None, *args):
        if target is None: return
        dx = target[0] - self.rect.centerx
        dy = target[1] - self.rect.centery
        dist = max(1, math.hypot(dx,dy))
        self.rect.x += int(self.speed * dx / dist)
        self.rect.y += int(self.speed * dy / dist)
        if self.hurt_timer > 0: self.hurt_timer -= 1

    def draw_health(self, surface):
        w = max(24, self.rect.width)
        x = self.rect.centerx - w//2; y = self.rect.top - 8
        pygame.draw.rect(surface, RED, (x,y,w,4))
        fill = int(w * (self.health/self.max_health))
        if fill>0: pygame.draw.rect(surface, GREEN, (x,y,fill,4))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, weapon):
        super().__init__()
        self.weapon = weapon
        if weapon == "pistol":
            self.image = PISTOL_BULLET; self.speed = 14; self.damage = WEAPONS["pistol"]["damage"]
        elif weapon == "shotgun":
            self.image = SHOTGUN_BULLET; self.speed = 11; self.damage = WEAPONS["shotgun"]["damage"]
        else:
            self.image = FIRE_IMG; self.speed = 8; self.damage = WEAPONS["flamethrower"]["damage"]
        self.rect = self.image.get_rect(center=pos)
        dx,dy = direction
        mag = max(1, math.hypot(dx,dy))
        self.vx = dx / mag * self.speed
        self.vy = dy / mag * self.speed

    def update(self, *args):
        self.rect.x += int(self.vx); self.rect.y += int(self.vy)
        if not WIN.get_rect().colliderect(self.rect): self.kill()

class Loot(pygame.sprite.Sprite):
    def __init__(self, pos, kind):
        super().__init__()
        self.kind = kind
        self.image = load_image_safe("health.png", (20,20), (120,220,180)) if kind=="health" else load_image_safe("ammo.png", (20,20), (220,200,60))
        self.rect = self.image.get_rect(center=pos)
        self.spawn = pygame.time.get_ticks()
    def update(self, *args):
        if pygame.time.get_ticks() - self.spawn > 20000: self.kill()

# -------- groups & initial player --------
player = Player(WIDTH//2, HEIGHT//2)
players = pygame.sprite.GroupSingle(player)
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
loots = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

# -------- state and scores --------
game_state = "menu"  # start at menu (we'll auto-detect when game starts)
score = 0
lives = 3
wave = 1
spawned_this_wave = 0
wave_target = 0

def set_state(s):
    global game_state
    game_state = s

# -------- highscores --------
def load_highscores():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE,"r") as f:
                txt = f.read().strip()
                if txt:
                    return [int(x) for x in txt.split(",") if x.strip().isdigit()]
        except:
            pass
    return []

def save_highscores(lst):
    try:
        with open(HIGHSCORE_FILE,"w") as f:
            f.write(",".join(str(x) for x in lst))
    except:
        pass

high_scores = load_highscores()
def add_highscore(v):
    global high_scores
    high_scores.append(v)
    high_scores = sorted(high_scores, reverse=True)[:5]
    save_highscores(high_scores)

# -------- wave helpers --------
def start_wave(n):
    global wave, spawned_this_wave, wave_target
    wave = n
    spawned_this_wave = 0
    wave_target = 3 + wave * 2

def spawn_next():
    global spawned_this_wave
    spawned_this_wave += 1
    is_boss = (spawned_this_wave == wave_target)
    side = random.choice(["left","right","top","bottom"])
    if side=="left": x,y = -40, random.randint(0, HEIGHT)
    elif side=="right": x,y = WIDTH+40, random.randint(0, HEIGHT)
    elif side=="top": x,y = random.randint(0, WIDTH), -40
    else: x,y = random.randint(0, WIDTH), HEIGHT + 40
    z = Zombie(x,y, is_boss)
    zombies.add(z); all_sprites.add(z)

def drop_loot_at(pos):
    if random.random() < 0.35:
        kind = random.choice(["health","ammo"])
        lt = Loot(pos, kind)
        loots.add(lt); all_sprites.add(lt)

# -------- mobile joystick vars --------
JOYSTICK_CENTER = (120, HEIGHT-140)
JOYSTICK_RADIUS = 42
KNOB_RADIUS = 22
knob_pos = JOYSTICK_CENTER
knob_active = False
mobile_input = {"left":False,"right":False,"shoot":False}
SHOOT_BTN = pygame.Rect(WIDTH-140, HEIGHT-160, 110, 110)

# -------- auto detect device (B: dual) --------
def auto_detect_device():
    plat = sys.platform.lower()
    if "android" in plat or "ios" in plat: return "mobile"
    info = pygame.display.Info()
    if info.current_w <= 640 or info.current_h <= 480: return "mobile"
    return "pc"

device_type = auto_detect_device()

# -------- reliable menu (auto-detect only for input, but still shows menu) --------
def main_menu():
    global device_type
    bg = MENU_BG

    labels = ["Play", "Settings", "High Scores", "Quit"]

    # moved menu options downward
    start_y = 300
    spacing = 75
    buttons = [
        pygame.Rect(WIDTH//2 - 150, start_y + i * spacing, 300, 60)
        for i in range(len(labels))
    ]

    while True:
        click_pos = None

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                click_pos = ev.pos

            if ev.type == pygame.KEYDOWN:
                device_type = "pc"
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        WIN.blit(bg, (0, 0))

        # Removed the big title completely
        # — nothing drawn at the top anymore —

        mx, my = pygame.mouse.get_pos()

        for i, rect in enumerate(buttons):
            clicked = draw_button(WIN, rect, labels[i], (mx, my), click_pos)
            if clicked:
                opt = labels[i]

                if opt == "Play":
                    device_type = auto_detect_device()
                    reset_game()
                    set_state("game")
                    return

                if opt == "Settings":
                    set_state("settings")
                    return

                if opt == "High Scores":
                    set_state("highscore")
                    return

                if opt == "Quit":
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        CLOCK.tick(60)


# -------- other screens --------
def settings_screen():
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                set_state("menu"); return
        WIN.fill(WHITE)
        draw_text_center(WIN, "Settings (press any key/click to return)", FONT, BLACK, HEIGHT//2)
        pygame.display.update(); CLOCK.tick(30)

def highscore_screen():
    global high_scores
    high_scores = load_highscores()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                set_state("menu"); return
        WIN.fill(WHITE)
        draw_text_center(WIN, "High Scores", BIG_FONT, BLACK, 120)
        for i,val in enumerate(high_scores):
            draw_text_center(WIN, f"{i+1}. {val}", FONT, BLACK, 220 + i*36)
        draw_text_center(WIN, "Press any key or click to return", SMALL_FONT, GRAY, 520)
        pygame.display.update(); CLOCK.tick(30)

def gameover_screen():
    add_highscore(score)
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    reset_game(); set_state("game"); return
                if ev.key == pygame.K_m:
                    reset_game(); set_state("menu"); return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                reset_game(); set_state("menu"); return
        WIN.fill(WHITE)
        draw_text_center(WIN, "GAME OVER", BIG_FONT, RED, 160)
        draw_text_center(WIN, f"Score: {score}", FONT, BLACK, 220)
        draw_text_center(WIN, f"Highscore: {high_scores[0] if high_scores else 0}", FONT, YELLOW, 260)
        draw_text_center(WIN, "Press R to Retry or click to return to menu", FONT, BLACK, 360)
        pygame.display.update(); CLOCK.tick(30)

# -------- reset game --------
def reset_game():
    global score, lives, player, players, zombies, bullets, loots, all_sprites, spawned_this_wave, wave_target, wave
    score = 0; lives = 3; wave = 1
    spawned_this_wave = 0; wave_target = 3 + wave*2
    zombies.empty(); bullets.empty(); loots.empty()
    all_sprites.empty()
    # recreate player and groups
    player.__init__(WIDTH//2, HEIGHT//2)  # reuse player instance to keep references
    players.add(player); all_sprites.add(player)

# -------- main gameplay loop --------
def run_game():
    global score, lives, wave, spawned_this_wave, wave_target, knob_active, knob_pos, mobile_input
    last_spawn = pygame.time.get_ticks()
    last_wave_finish = 0
    start_wave(1)
    mouse_shoot = False

    while game_state == "game":
        dt = CLOCK.tick(FPS)
        now = pygame.time.get_ticks()
        click_pos = None
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                # keyboard -> PC
                if ev.key == pygame.K_ESCAPE:
                    add_highscore(score); set_state("menu"); return
                if ev.key == pygame.K_1: player.switch_weapon(0)
                if ev.key == pygame.K_2: player.switch_weapon(1)
                if ev.key == pygame.K_3: player.switch_weapon(2)
            if ev.type == pygame.MOUSEWHEEL:
                player.switch_weapon_scroll(-ev.y)
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                click_pos = ev.pos
                if device_type == "pc":
                    mouse_shoot = True
                else:
                    mx,my = ev.pos
                    if (mx - JOYSTICK_CENTER[0])**2 + (my - JOYSTICK_CENTER[1])**2 <= JOYSTICK_RADIUS**2:
                        knob_active = True; knob_pos = ev.pos
                    if SHOOT_BTN.collidepoint(ev.pos):
                        mobile_input["shoot"] = True
            if ev.type == pygame.MOUSEBUTTONUP:
                if device_type == "pc": mouse_shoot = False
                else:
                    knob_active = False
                    mobile_input["left"] = mobile_input["right"] = False
                    mobile_input["shoot"] = False
            if ev.type == pygame.MOUSEMOTION and knob_active:
                mx,my = ev.pos; ox,oy = JOYSTICK_CENTER
                vx,vy = mx-ox, my-oy
                d = math.hypot(vx,vy)
                if d > JOYSTICK_RADIUS: vx,vy = vx/d*JOYSTICK_RADIUS, vy/d*JOYSTICK_RADIUS
                knob_pos = (int(ox+vx), int(oy+vy))
                mobile_input["left"] = vx < -10; mobile_input["right"] = vx > 10

        # spawn zombies
        if spawned_this_wave < wave_target and now - last_spawn >= SPAWN_DELAY:
            spawn_next(); last_spawn = now

        # wave complete -> next wave after short pause
        if spawned_this_wave >= wave_target and len(zombies) == 0:
            if last_wave_finish == 0:
                last_wave_finish = now
            elif now - last_wave_finish > 800:
                start_wave(wave + 1); last_wave_finish = 0; last_spawn = pygame.time.get_ticks()

        # shooting checks
        is_shooting = False
        aim = pygame.mouse.get_pos()
        if device_type == "pc":
            is_shooting = pygame.mouse.get_pressed()[0] or mouse_shoot
        else:
            is_shooting = mobile_input.get("shoot", False)

        if is_shooting:
            weapon = player.weapon
            if now - player.last_shot >= WEAPONS[weapon]["rate"]:
                if weapon == "shotgun":
                    pellets = 5
                    angle = math.atan2(aim[1] - player.rect.centery, aim[0] - player.rect.centerx)
                    for _ in range(pellets):
                        spread = random.uniform(-0.28, 0.28)
                        dx = math.cos(angle + spread); dy = math.sin(angle + spread)
                        b = Bullet(player.rect.center, (dx,dy), "shotgun"); bullets.add(b); all_sprites.add(b)
                else:
                    dx = aim[0] - player.rect.centerx; dy = aim[1] - player.rect.centery
                    b = Bullet(player.rect.center, (dx,dy), weapon); bullets.add(b); all_sprites.add(b)
                player.last_shot = now
                if device_type == "mobile":
                    mobile_input["shoot"] = False

        # updates
        if device_type == "mobile":
            player.update(keys=None, mobile_input=mobile_input)
        else:
            player.update(keys=pygame.key.get_pressed())

        for z in list(zombies): z.update(target=player.rect.center)
        bullets.update(); loots.update()

        # bullet collisions -> zombies
        for b in list(bullets):
            hit = False
            for z in list(zombies):
                if z.rect.colliderect(b.rect):
                    z.health -= b.damage
                    z.hurt_timer = 6
                    hit = True
                    if z.health <= 0:
                        score += (80 if z.is_boss else 10)
                        drop_loot_at(z.rect.center)
                        z.kill()
                    b.kill()
                    break
            if hit: continue

        # player <-> zombie collisions
        collisions = [z for z in zombies if z.rect.colliderect(player.rect)]
        if collisions:
            player.take_damage(2 * len(collisions))

        # pickup loot
        picked = pygame.sprite.spritecollide(player, loots, True)
        for p in picked:
            if p.kind == "health":
                player.health = min(player.max_health, player.health + 35)
            else:
                WEAPONS["shotgun"]["ammo"] += 6
                WEAPONS["flamethrower"]["ammo"] += 4

        # draw
        WIN.blit(BG_IMG, (0,0))

        for z in zombies:
            if z.hurt_timer > 0:
                s = z.image.copy(); s.fill((255,80,80,80), special_flags=pygame.BLEND_RGBA_ADD); WIN.blit(s, z.rect.topleft)
            else:
                WIN.blit(z.image, z.rect.topleft)
            z.draw_health(WIN)

        for b in bullets: WIN.blit(b.image, b.rect.topleft)
        for lt in loots: WIN.blit(lt.image, lt.rect.topleft)

        WIN.blit(player.image, (player.rect.x, player.rect.y + int(player.bob)))
        player.draw_health(WIN)

        # HUD
        WIN.blit(FONT.render(f"Score: {score}", True, BLACK), (WIDTH-220, 12))
        WIN.blit(FONT.render(f"Lives: {lives}", True, BLACK), (WIDTH-220, 36))
        WIN.blit(FONT.render(f"Wave: {wave}", True, BLACK), (WIDTH-220, 60))

        wy = 12
        for i,w in enumerate(WEAPON_LIST):
            color = YELLOW if i==player.weapon_index else BLACK
            ammo_str = "" if WEAPONS[w]["ammo"] >= 999 else f"({WEAPONS[w]['ammo']})"
            WIN.blit(FONT.render(f"{i+1}. {w.capitalize()} {ammo_str}", True, color), (8,wy)); wy += 26

        # mobile UI only if detected mobile
        if device_type == "mobile":
            pygame.draw.circle(WIN, (40,40,40), JOYSTICK_CENTER, JOYSTICK_RADIUS)
            pygame.draw.circle(WIN, (200,200,200), knob_pos, KNOB_RADIUS)
            rounded_rect(WIN, (SHOOT_BTN.x, SHOOT_BTN.y, SHOOT_BTN.w, SHOOT_BTN.h), (200,50,50), 18)
            s = FONT.render("SHOOT", True, WHITE); WIN.blit(s, (SHOOT_BTN.centerx - s.get_width()//2, SHOOT_BTN.centery - s.get_height()//2))

        pygame.display.update()

        if lives <= 0:
            add_highscore(score); set_state("gameover"); return

# -------- main loop --------
def main():
    global device_type
    device_type = auto_detect_device()
    while True:
        if game_state == "menu":
            main_menu()
        elif game_state == "settings":
            settings_screen()
        elif game_state == "highscore":
            highscore_screen()
        elif game_state == "game":
            run_game()
        elif game_state == "gameover":
            gameover_screen()
        else:
            set_state("menu")

if __name__ == "__main__":
    # initialize score/lives
    score = 0; lives = 3
    main()
