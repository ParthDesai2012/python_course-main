import pygame, sys, math, random

pygame.init()

# ================= AUTO-DETECT DEVICE =================
def auto_detect_device():
    plat = sys.platform.lower()
    if "android" in plat or "ios" in plat:
        return "mobile"
    info = pygame.display.Info()
    if info.current_w <= 640 or info.current_h <= 480:
        return "mobile"
    return "pc"

device_type = auto_detect_device()

# ================= SCREEN =================
if device_type == "mobile":
    INFO = pygame.display.Info()
    WIDTH, HEIGHT = INFO.current_w, INFO.current_h
else:
    WIDTH, HEIGHT = 900, 650

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")
CLOCK = pygame.time.Clock()
FPS = 60

# ================= SCALING =================
BASE_W = 900
UI_SCALE = WIDTH / BASE_W

def s(v): return int(v * UI_SCALE)

# ================= COLORS =================
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,40,40)
GREEN = (40,200,40)
YELLOW = (240,200,40)
PURPLE = (180,40,180)
ORANGE = (255,140,0)
GRAY = (140,140,140)
ACCENT = (70,160,255)
DARK_BG = (25, 25, 35)

# ================= FONTS =================
FONT = pygame.font.SysFont("arial", s(18))
BIG = pygame.font.SysFont("arial", s(36))
SMALL = pygame.font.SysFont("arial", s(14))
TINY = pygame.font.SysFont("arial", s(12))

# ================= GAME STATE =================
game_state = "menu"
score = 0
coins = 0
lives = 3
wave = 1
kills = 0
high_scores = []
ads_enabled = True
games_played = 0

# ================= PLAYER =================
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, s(40), s(40))
        self.speed = s(6)
        self.max_health = 100
        self.health = self.max_health
        self.invulnerable_timer = 0
        self.bob = 0
        self.bob_dir = 1

    def update(self, move_vec):
        self.rect.x += int(move_vec[0] * self.speed)
        self.rect.y += int(move_vec[1] * self.speed)
        self.rect.clamp_ip(WIN.get_rect())
        
        self.bob += 0.15 * self.bob_dir
        if abs(self.bob) > 2:
            self.bob_dir *= -1
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def take_damage(self, amt):
        global lives, game_state
        if self.invulnerable_timer > 0:
            return
        self.health -= amt
        self.invulnerable_timer = 60
        create_particles(self.rect.centerx, self.rect.centery, RED, 12)
        if self.health <= 0:
            lives -= 1
            if lives <= 0:
                game_state = "gameover"
            else:
                self.health = self.max_health
                self.invulnerable_timer = 120
                self.rect.center = (WIDTH//2, HEIGHT//2)

    def draw(self, surface):
        if self.invulnerable_timer == 0 or self.invulnerable_timer % 10 < 5:
            y_offset = int(self.bob)
            pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y + y_offset, self.rect.w, self.rect.h))
            pygame.draw.rect(surface, WHITE, (self.rect.x, self.rect.y + y_offset, self.rect.w, self.rect.h), 2)

    def draw_health(self, surface):
        bar_w, bar_h = s(44), s(7)
        x = self.rect.centerx - bar_w//2
        y = self.rect.top - s(12)
        pygame.draw.rect(surface, RED, (x, y, bar_w, bar_h))
        health_fill = int(bar_w * (self.health / self.max_health))
        if health_fill > 0:
            pygame.draw.rect(surface, GREEN, (x, y, health_fill, bar_h))

player = Player(WIDTH//2, HEIGHT//2)

# ================= ZOMBIES =================
zombies = []

def spawn_wave():
    global zombies
    count = 3 + wave * 2
    zombies = []
    for i in range(count):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x, y = random.randint(0, WIDTH), -50
        elif side == "bottom":
            x, y = random.randint(0, WIDTH), HEIGHT+50
        elif side == "left":
            x, y = -50, random.randint(0, HEIGHT)
        else:
            x, y = WIDTH+50, random.randint(0, HEIGHT)
        
        zombie_type = random.choices(
            ["normal", "fast", "tank", "boss"],
            weights=[70, 20, 8, 2] if wave > 2 else [90, 10, 0, 0]
        )[0]
        
        if zombie_type == "boss":
            hp, speed, size, color = 300, 1.2, s(50), RED
        elif zombie_type == "tank":
            hp, speed, size, color = 150, 1.0, s(45), (100,30,30)
        elif zombie_type == "fast":
            hp, speed, size, color = 40, 2.5, s(30), PURPLE
        else:
            hp, speed, size, color = 60, 1.5, s(34), (160,60,60)
        
        zombies.append({
            "rect": pygame.Rect(x, y, size, size),
            "hp": hp,
            "max_hp": hp,
            "speed": speed,
            "type": zombie_type,
            "color": color,
            "hurt_timer": 0
        })

# ================= BULLETS =================
bullets = []
fire_cooldown = 0
FIRE_RATE = 8

# ================= PARTICLES =================
particles = []

def create_particles(x, y, color, count=8):
    for _ in range(count):
        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(2, 6)
        particles.append({
            "x": x,
            "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "color": color,
            "life": 30
        })

# ================= POWERUPS =================
powerups = []
POWERUP_TYPES = ["health", "rapid_fire", "damage", "coin"]
active_powerups = {"rapid_fire": 0, "damage": 0}

def spawn_powerup(x, y):
    if random.random() < 0.4:
        powerups.append({
            "rect": pygame.Rect(x, y, s(25), s(25)),
            "type": random.choice(POWERUP_TYPES),
            "lifetime": 300
        })

# ================= JOYSTICKS =================
LEFT_CENTER = (s(100), HEIGHT - s(120))
RIGHT_CENTER = (WIDTH - s(100), HEIGHT - s(120))
JOY_RADIUS = s(50)
KNOB_RADIUS = s(22)

left_knob = LEFT_CENTER
right_knob = RIGHT_CENTER
left_active = right_active = False
move_vec = [0,0]
aim_vec = [0,0]

# ================= AD SYSTEM =================
ad_watching = False
ad_watch_timer = 0
ad_reward_type = None

def show_rewarded_ad(reward_type):
    global ad_watching, ad_watch_timer, ad_reward_type
    if ads_enabled:
        ad_watching = True
        ad_watch_timer = 180
        ad_reward_type = reward_type
        return True
    return False

def complete_ad_watch():
    global ad_watching, coins, lives, player
    if ad_reward_type == "continue":
        player.health = player.max_health
        lives += 1
    elif ad_reward_type == "coins":
        coins += 50
    elif ad_reward_type == "powerup":
        active_powerups["rapid_fire"] = 600
        active_powerups["damage"] = 600
    ad_watching = False

# ================= UI HELPERS =================
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

def draw_ad_overlay():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    WIN.blit(overlay, (0, 0))
    
    ad_w, ad_h = s(600), s(400)
    ad_rect = pygame.Rect(WIDTH//2 - ad_w//2, HEIGHT//2 - ad_h//2, ad_w, ad_h)
    rounded_rect(WIN, (ad_rect.x, ad_rect.y, ad_rect.w, ad_rect.h), (40,40,50), 20)
    pygame.draw.rect(WIN, ACCENT, ad_rect, 3, border_radius=20)
    
    draw_text_center(WIN, "📺 SIMULATED AD", BIG, WHITE, HEIGHT//2 - s(80))
    draw_text_center(WIN, "(In real game, this would be a video ad)", FONT, GRAY, HEIGHT//2 - s(40))
    draw_text_center(WIN, "Ad Network: AdMob / Unity Ads", SMALL, GRAY, HEIGHT//2)
    
    seconds_left = (ad_watch_timer // 60) + 1
    draw_text_center(WIN, f"⏱️ Watch for {seconds_left} more seconds...", FONT, YELLOW, HEIGHT//2 + s(40))
    
    progress = 1 - (ad_watch_timer / 180)
    bar_w = s(400)
    bar_x = WIDTH//2 - bar_w//2
    bar_y = HEIGHT//2 + s(80)
    pygame.draw.rect(WIN, (60,60,60), (bar_x, bar_y, bar_w, s(20)))
    pygame.draw.rect(WIN, GREEN, (bar_x, bar_y, int(bar_w * progress), s(20)))

# ================= FUNCTIONS =================
def clamp_vec(vx, vy, maxlen):
    mag = math.hypot(vx, vy)
    if mag > maxlen:
        vx = vx/mag * maxlen
        vy = vy/mag * maxlen
    return vx, vy

def reset_game():
    global player, score, lives, wave, kills, zombies, bullets, powerups, particles, coins
    global fire_cooldown, active_powerups, move_vec, aim_vec, games_played
    global left_knob, right_knob, left_active, right_active
    
    player = Player(WIDTH//2, HEIGHT//2)
    score = 0
    lives = 3
    wave = 1
    kills = 0
    zombies = []
    bullets = []
    powerups = []
    particles = []
    fire_cooldown = 0
    active_powerups = {"rapid_fire": 0, "damage": 0}
    move_vec = [0, 0]
    aim_vec = [0, 0]
    left_knob = LEFT_CENTER
    right_knob = RIGHT_CENTER
    left_active = right_active = False
    games_played += 1
    
    spawn_wave()

# ================= MENU =================
def main_menu():
    labels = ["▶ Play", "🏆 High Scores", "❌ Quit"]
    start_y = s(300)
    spacing = s(75)
    buttons = [
        pygame.Rect(WIDTH//2 - s(150), start_y + i * spacing, s(300), s(60))
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
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        WIN.fill(DARK_BG)
        
        title = BIG.render("ZOMBIE SURVIVAL", True, RED)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, s(120)))
        
        subtitle = FONT.render("Survive the waves!", True, WHITE)
        WIN.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, s(180)))
        
        coin_text = FONT.render(f"💰 Coins: {coins}", True, YELLOW)
        WIN.blit(coin_text, (WIDTH//2 - coin_text.get_width()//2, s(220)))

        mx, my = pygame.mouse.get_pos()
        for i, rect in enumerate(buttons):
            clicked = draw_button(WIN, rect, labels[i], (mx, my), click_pos)
            if clicked:
                if i == 0:
                    reset_game()
                    return
                elif i == 1:
                    highscore_screen()
                elif i == 2:
                    pygame.quit()
                    sys.exit()

        info_y = HEIGHT - s(80)
        info_texts = [
            "💡 Watch ads to earn coins & bonuses!",
            "🎮 Left stick = Move | Right stick = Aim & Shoot"
        ]
        for i, txt in enumerate(info_texts):
            info = SMALL.render(txt, True, GRAY)
            WIN.blit(info, (WIDTH//2 - info.get_width()//2, info_y + i*s(20)))

        pygame.display.update()
        CLOCK.tick(60)

def highscore_screen():
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return
        
        WIN.fill(DARK_BG)
        draw_text_center(WIN, "🏆 HIGH SCORES", BIG, RED, s(120))
        
        if high_scores:
            for i, val in enumerate(high_scores[:5]):
                medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
                draw_text_center(WIN, f"{medal} {val}", FONT, WHITE, s(220) + i*s(36))
        else:
            draw_text_center(WIN, "No scores yet!", FONT, GRAY, s(280))
        
        draw_text_center(WIN, "Press any key or tap to return", SMALL, GRAY, HEIGHT - s(50))
        pygame.display.update()
        CLOCK.tick(30)

def gameover_screen():
    global high_scores, games_played
    high_scores.append(score)
    high_scores = sorted(high_scores, reverse=True)[:5]
    
    show_interstitial = ads_enabled and (games_played % 3 == 0)
    if show_interstitial:
        show_interstitial_ad()
    
    while True:
        click_pos = None
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    reset_game()
                    return
                if ev.key == pygame.K_m:
                    return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                click_pos = ev.pos
        
        WIN.fill(DARK_BG)
        draw_text_center(WIN, "💀 GAME OVER", BIG, RED, s(100))
        draw_text_center(WIN, f"Score: {score}", FONT, WHITE, s(180))
        draw_text_center(WIN, f"Wave: {wave} | Kills: {kills}", FONT, WHITE, s(220))
        draw_text_center(WIN, f"Coins Earned: +{score//10}", FONT, YELLOW, s(260))
        draw_text_center(WIN, f"Best: {high_scores[0] if high_scores else 0}", FONT, ORANGE, s(300))
        
        button_w, button_h = s(250), s(50)
        continue_btn = pygame.Rect(WIDTH//2 - button_w//2, s(360), button_w, button_h)
        coins_btn = pygame.Rect(WIDTH//2 - button_w//2, s(420), button_w, button_h)
        
        mx, my = pygame.mouse.get_pos()
        if draw_button(WIN, continue_btn, "📺 Watch Ad → Continue", (mx, my), click_pos):
            if show_rewarded_ad("continue"):
                while ad_watching:
                    ad_update()
                reset_game()
                return
        
        if draw_button(WIN, coins_btn, "📺 Watch Ad → +50 Coins", (mx, my), click_pos):
            if show_rewarded_ad("coins"):
                while ad_watching:
                    ad_update()
        
        draw_text_center(WIN, "Press R to Retry | Tap to Menu", SMALL, GRAY, HEIGHT - s(50))
        
        pygame.display.update()
        CLOCK.tick(30)

def show_interstitial_ad():
    timer = 120
    while timer > 0:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        WIN.fill(BLACK)
        draw_text_center(WIN, "📺 ADVERTISEMENT", BIG, WHITE, HEIGHT//2 - s(60))
        draw_text_center(WIN, "(Simulated Interstitial Ad)", FONT, GRAY, HEIGHT//2)
        draw_text_center(WIN, f"Closing in {timer//60 + 1}...", SMALL, YELLOW, HEIGHT//2 + s(60))
        
        pygame.display.update()
        CLOCK.tick(60)
        timer -= 1

def ad_update():
    global ad_watch_timer, ad_watching
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    draw_ad_overlay()
    pygame.display.update()
    CLOCK.tick(60)
    
    ad_watch_timer -= 1
    if ad_watch_timer <= 0:
        complete_ad_watch()

# ================= MAIN GAME LOOP =================
def run_game():
    global score, lives, wave, kills, fire_cooldown, move_vec, aim_vec, game_state, coins
    global left_knob, right_knob, left_active, right_active
    
    while game_state == "game":
        CLOCK.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    return

            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                # Check if clicking on joysticks
                if math.hypot(mx-LEFT_CENTER[0], my-LEFT_CENTER[1]) < JOY_RADIUS:
                    left_active = True
                elif math.hypot(mx-RIGHT_CENTER[0], my-RIGHT_CENTER[1]) < JOY_RADIUS:
                    right_active = True

            if e.type == pygame.MOUSEBUTTONUP:
                left_active = right_active = False
                left_knob = LEFT_CENTER
                right_knob = RIGHT_CENTER

            if e.type == pygame.MOUSEMOTION:
                mx, my = e.pos
                if left_active:
                    vx, vy = mx-LEFT_CENTER[0], my-LEFT_CENTER[1]
                    vx, vy = clamp_vec(vx, vy, JOY_RADIUS)
                    left_knob = (LEFT_CENTER[0]+vx, LEFT_CENTER[1]+vy)
                if right_active:
                    vx, vy = mx-RIGHT_CENTER[0], my-RIGHT_CENTER[1]
                    vx, vy = clamp_vec(vx, vy, JOY_RADIUS)
                    right_knob = (RIGHT_CENTER[0]+vx, RIGHT_CENTER[1]+vy)

        # KEYBOARD CONTROLS (WASD or Arrow Keys)
        keys = pygame.key.get_pressed()
        keyboard_move = [0, 0]
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            keyboard_move[1] -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            keyboard_move[1] += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            keyboard_move[0] -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            keyboard_move[0] += 1
        
        # MOUSE AIM & SHOOT
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_aim = [0, 0]
        
        # Only use mouse for aiming if not clicking on joysticks
        if mouse_pressed and not left_active and not right_active:
            # Check if mouse is far enough from joysticks to be shooting
            if (math.hypot(mouse_x-LEFT_CENTER[0], mouse_y-LEFT_CENTER[1]) > JOY_RADIUS + 20 and
                math.hypot(mouse_x-RIGHT_CENTER[0], mouse_y-RIGHT_CENTER[1]) > JOY_RADIUS + 20):
                mouse_aim = [mouse_x - player.rect.centerx, mouse_y - player.rect.centery]
        
        # COMBINE INPUTS (Joystick OR Keyboard)
        if left_active:
            vx, vy = left_knob[0] - LEFT_CENTER[0], left_knob[1] - LEFT_CENTER[1]
            move_vec = [vx/JOY_RADIUS, vy/JOY_RADIUS]
        elif keyboard_move != [0, 0]:
            move_vec = keyboard_move
        else:
            move_vec = [0, 0]
        
        # AIM: Joystick OR Mouse
        if right_active:
            vx, vy = right_knob[0] - RIGHT_CENTER[0], right_knob[1] - RIGHT_CENTER[1]
            aim_vec = [vx, vy]
        elif mouse_aim != [0, 0]:
            aim_vec = mouse_aim
        else:
            aim_vec = [0, 0]

        if fire_cooldown > 0:
            fire_cooldown -= 1
        for key in active_powerups:
            if active_powerups[key] > 0:
                active_powerups[key] -= 1

        player.update(move_vec)

        # Update zombies - move toward player
        for z in zombies[:]:
            dx = player.rect.centerx - z["rect"].centerx
            dy = player.rect.centery - z["rect"].centery
            d = max(1, math.hypot(dx, dy))
            move_x = int(dx/d * z["speed"])
            move_y = int(dy/d * z["speed"])
            
            z["rect"].x += move_x
            z["rect"].y += move_y
            
            if z["hurt_timer"] > 0:
                z["hurt_timer"] -= 1
            
            if z["rect"].colliderect(player.rect):
                player.take_damage(10)

        current_fire_rate = FIRE_RATE // 2 if active_powerups["rapid_fire"] > 0 else FIRE_RATE
        if aim_vec != [0, 0] and fire_cooldown == 0:
            fire_cooldown = current_fire_rate
            mag = math.hypot(aim_vec[0], aim_vec[1])
            if mag > 0:
                bullets.append({
                    "rect": pygame.Rect(player.rect.centerx, player.rect.centery, s(8), s(8)),
                    "vx": (aim_vec[0]/mag) * s(12),
                    "vy": (aim_vec[1]/mag) * s(12),
                    "damage": 25 if active_powerups["damage"] > 0 else 15
                })

        for b in bullets[:]:
            b["rect"].x += b["vx"]
            b["rect"].y += b["vy"]
            
            if not WIN.get_rect().colliderect(b["rect"]):
                bullets.remove(b)
                continue
            
            for z in zombies[:]:
                if b["rect"].colliderect(z["rect"]):
                    z["hp"] -= b["damage"]
                    z["hurt_timer"] = 6
                    create_particles(b["rect"].centerx, b["rect"].centery, z["color"], 5)
                    if b in bullets:
                        bullets.remove(b)
                    if z["hp"] <= 0:
                        points = {"normal": 10, "fast": 15, "tank": 25, "boss": 100}
                        score += points.get(z["type"], 10)
                        coins += 1
                        kills += 1
                        create_particles(z["rect"].centerx, z["rect"].centery, z["color"], 15)
                        spawn_powerup(z["rect"].centerx, z["rect"].centery)
                        zombies.remove(z)
                    break

        for p in particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
            if p["life"] <= 0:
                particles.remove(p)

        for pw in powerups[:]:
            pw["lifetime"] -= 1
            if pw["lifetime"] <= 0:
                powerups.remove(pw)
                continue
            
            if pw["rect"].colliderect(player.rect):
                if pw["type"] == "health":
                    player.health = min(player.max_health, player.health + 30)
                elif pw["type"] == "rapid_fire":
                    active_powerups["rapid_fire"] = 300
                elif pw["type"] == "damage":
                    active_powerups["damage"] = 300
                elif pw["type"] == "coin":
                    coins += 5
                create_particles(pw["rect"].centerx, pw["rect"].centery, YELLOW, 10)
                powerups.remove(pw)

        if not zombies:
            wave += 1
            spawn_wave()

        # ================= DRAW =================
        WIN.fill((20, 20, 30))
        
        for i in range(0, WIDTH, s(50)):
            pygame.draw.line(WIN, (30, 30, 40), (i, 0), (i, HEIGHT))
        for i in range(0, HEIGHT, s(50)):
            pygame.draw.line(WIN, (30, 30, 40), (0, i), (WIDTH, i))

        for p in particles:
            pygame.draw.circle(WIN, p["color"], (int(p["x"]), int(p["y"])), s(3))

        for b in bullets:
            pygame.draw.circle(WIN, YELLOW, b["rect"].center, s(4))

        for pw in powerups:
            colors = {"health": GREEN, "rapid_fire": ORANGE, "damage": PURPLE, "coin": YELLOW}
            color = colors[pw["type"]]
            pygame.draw.rect(WIN, color, pw["rect"])
            pygame.draw.rect(WIN, WHITE, pw["rect"], 2)
            icons = {"health": "❤️", "rapid_fire": "⚡", "damage": "💥", "coin": "💰"}
            icon = TINY.render(icons[pw["type"]], True, WHITE)
            WIN.blit(icon, (pw["rect"].centerx - icon.get_width()//2, pw["rect"].centery - icon.get_height()//2))

        player.draw(WIN)
        player.draw_health(WIN)

        # Draw zombies
        for z in zombies:
            if z["hurt_timer"] > 0:
                tint_color = tuple(min(255, c + 100) for c in z["color"])
                pygame.draw.rect(WIN, tint_color, z["rect"])
            else:
                pygame.draw.rect(WIN, z["color"], z["rect"])
            pygame.draw.rect(WIN, WHITE, z["rect"], 2)
            
            # Health bar above zombie
            bar_width = z["rect"].width
            health_pct = z["hp"] / z["max_hp"]
            bar_rect = pygame.Rect(z["rect"].x, z["rect"].y - s(8), int(bar_width * health_pct), s(4))
            pygame.draw.rect(WIN, RED, bar_rect)

        hud_y = 10
        WIN.blit(FONT.render(f"Score: {score}", True, WHITE), (10, hud_y))
        WIN.blit(FONT.render(f"💰 {coins}", True, YELLOW), (10, hud_y + s(30)))
        WIN.blit(FONT.render(f"Wave: {wave}", True, ORANGE), (10, hud_y + s(60)))
        WIN.blit(FONT.render(f"Kills: {kills}", True, WHITE), (10, hud_y + s(90)))
        WIN.blit(FONT.render(f"Lives: {lives}", True, RED), (10, hud_y + s(120)))
        
        bar_x = 10
        bar_y = hud_y + s(150)
        pygame.draw.rect(WIN, (60, 60, 60), (bar_x, bar_y, s(150), s(20)))
        health_width = int(s(150) * (player.health / player.max_health))
        health_color = GREEN if player.health > 50 else ORANGE if player.health > 25 else RED
        pygame.draw.rect(WIN, health_color, (bar_x, bar_y, health_width, s(20)))
        pygame.draw.rect(WIN, WHITE, (bar_x, bar_y, s(150), s(20)), 2)
        
        if active_powerups["rapid_fire"] > 0:
            WIN.blit(SMALL.render(f"⚡ Rapid: {active_powerups['rapid_fire']//60}s", True, ORANGE), (10, bar_y + s(30)))
        if active_powerups["damage"] > 0:
            WIN.blit(SMALL.render(f"💥 Damage: {active_powerups['damage']//60}s", True, PURPLE), (10, bar_y + s(50)))

        # Left joystick
        pygame.draw.circle(WIN, (50, 50, 60), LEFT_CENTER, JOY_RADIUS, 3)
        pygame.draw.circle(WIN, (100, 100, 110), LEFT_CENTER, JOY_RADIUS - 5, 1)
        pygame.draw.circle(WIN, (180, 180, 200), left_knob, KNOB_RADIUS)
        move_label = TINY.render("MOVE", True, GRAY)
        WIN.blit(move_label, (LEFT_CENTER[0] - move_label.get_width()//2, LEFT_CENTER[1] + JOY_RADIUS + s(10)))

        # Right joystick
        pygame.draw.circle(WIN, (80, 50, 50), RIGHT_CENTER, JOY_RADIUS, 3)
        pygame.draw.circle(WIN, (120, 70, 70), RIGHT_CENTER, JOY_RADIUS - 5, 1)
        pygame.draw.circle(WIN, (220, 180, 180), right_knob, KNOB_RADIUS)
        shoot_label = TINY.render("AIM & SHOOT", True, GRAY)
        WIN.blit(shoot_label, (RIGHT_CENTER[0] - shoot_label.get_width()//2, RIGHT_CENTER[1] + JOY_RADIUS + s(10)))

        pygame.display.update()

# ================= MAIN =================
def main():
    global game_state
    # Initialize first wave
    spawn_wave()
    
    while True:
        if game_state == "menu":
            main_menu()
            game_state = "game"
        elif game_state == "game":
            run_game()
            if game_state == "gameover":
                gameover_screen()
                game_state = "menu"

if __name__ == "__main__":
    main()
    