import pygame
import random
import sys
# --- 1. INITIALIZATION & SETUP ---

pygame.init()
pygame.mixer.init()

# Game Constants
WIDTH, HEIGHT = 900, 560
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boba Blaster")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
font_large = pygame.font.SysFont("Arial", 40)
font_small = pygame.font.SysFont("Arial", 25)

# Load Media
manual_img = pygame.image.load("images/user_manual2.jpg").convert()
manual_img = pygame.transform.scale(manual_img, (WIDTH, HEIGHT))
bg_img = pygame.image.load("images/5.jpg").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# Load Sounds
shoot_sound = pygame.mixer.Sound("sound/pew-pew-lame-sound-effect.mp3")
yey_sound = pygame.mixer.Sound("sound/children-saying-yay-praise-and-worship-jesus-299607.mp3")

# Load Sprites
milktea_img = pygame.image.load("images/1-removebg-preview (2).png").convert_alpha()
milktea_img = pygame.transform.scale(milktea_img, (200, 200))

pearl_img = pygame.image.load("images/2-removebg-preview (1).png").convert_alpha()
pearl_img = pygame.transform.scale(pearl_img, (30, 30))

coffee_img = pygame.image.load("images/3-removebg-preview (1).png").convert_alpha()
coffee_img = pygame.transform.scale(coffee_img, (50, 50))

pop_img = pygame.image.load("images/sparkle.png").convert_alpha()
pop_img = pygame.transform.scale(pop_img, (30, 30))

powerup_img = pygame.image.load("images/powerup.png").convert_alpha()
powerup_img = pygame.transform.scale(powerup_img, (60, 60))

bomb_img = pygame.image.load("images/bomb.png").convert_alpha()
bomb_img = pygame.transform.scale(bomb_img, (60, 60))

# Character Mappings
CHARACTERS = {
    "bunny": "images/bunny.png", "capybara": "images/capy.png", "cat": "images/kitty.png",
}
MISSION_CHARACTERS = {
    "bunny": "images/bunnym.png", "capybara": "images/capym.png", "cat": "images/kittym.png",
}

# ----------------------------------------------------
# --- 2. HELPER FUNCTIONS & CLASSES ---
# ----------------------------------------------------

# --- Confetti Logic ---
confetti_particles = []
def spawn_confetti():
    for _ in range(100):
        confetti_particles.append({
            "x": random.randint(0, WIDTH), "y": random.randint(-HEIGHT, 0),
            "speed_y": random.uniform(2, 6), "speed_x": random.uniform(-2, 2),
            "color": random.choice([(255,105,180), (255,255,255), (255,182,193), (255,200,255), (255,230,230)]),
            "size": random.randint(3, 7)
        })
def update_confetti():
    for c in confetti_particles:
        c["y"] += c["speed_y"]
        c["x"] += c["speed_x"]
    return [c for c in confetti_particles if c["y"] < HEIGHT + 20]

# --- Pop Effect Class (used for visual feedback on hits) ---
class PopEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, image, duration=15):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = duration
        
    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

# --- Game Sprite Classes (Simplified) ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.fire_rate = 150 
        self.last_shot = pygame.time.get_ticks()
        self.powerup_active = False
        self.powerup_timer = 0
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)

    def shoot(self, pearl_image):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            self.last_shot = now
            pearls = []
            if self.powerup_active:
                pearls.append(Pearl(self.rect.centerx - 20, self.rect.top + 20, pearl_image))
                pearls.append(Pearl(self.rect.centerx + 20, self.rect.top + 20, pearl_image))
                pearls.append(Pearl(self.rect.centerx, self.rect.top, pearl_image))
            else:
                pearls.append(Pearl(self.rect.centerx, self.rect.top, pearl_image))
            return pearls
        return []

class Pearl(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8
        
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class CoffeeBean(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class PowerUp(CoffeeBean):
    pass 

class Bomb(CoffeeBean):
    def __init__(self, x, y, image, speed):
        super().__init__(x, y, image, speed + 1)


# ----------------------------------------------------
# --- 3. CORE GAME FUNCTIONS ---
# ----------------------------------------------------

def show_manual():
    # ... (Your original manual function logic remains here)
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    alpha = 255

    font_manual = pygame.font.SysFont("Arial", 28)
    text = font_manual.render("Press ENTER to Start ✨", True, (255, 255, 255))
    pygame.event.clear()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        screen.blit(manual_img, (0, 0))
        if alpha > 0:
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            alpha -= 4
        if pygame.time.get_ticks() % 1000 < 600:
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 70))
        pygame.display.flip()
        clock.tick(60)

def select_character():
    selected = None
    float_offset = 0
    float_direction = 1

    while not selected:
        screen.blit(bg_img, (0, 0))

        # Title
        hint = font_large.render("Select your character!", True, (255, 255, 255))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 400))
        
        # Floating animation
        float_offset += float_direction * 0.5
        if float_offset > 5 or float_offset < -5:
            float_direction *= -1

        # Load and scale character images
        bunny = pygame.transform.scale(pygame.image.load(CHARACTERS["bunny"]).convert_alpha(), (150, 150))
        capy = pygame.transform.scale(pygame.image.load(CHARACTERS["capybara"]).convert_alpha(), (150, 150))
        kitty = pygame.transform.scale(pygame.image.load(CHARACTERS["cat"]).convert_alpha(), (150, 150))

        # Positions
        screen.blit(bunny, (150, 150 + float_offset))
        screen.blit(capy, (375, 150 + float_offset))
        screen.blit(kitty, (600, 150 + float_offset))

        # Labels
        def draw_label(text, x, y):
            label = font_small.render(text, True, (255, 255, 255))
            padding = 10
            bg_rect = pygame.Rect(x - padding, y - padding, label.get_width() + padding * 2, label.get_height() + padding * 2)
            pygame.draw.rect(screen, (217,2,125), bg_rect, border_radius=10)
            screen.blit(label, (x, y))

        draw_label("1 - BUNNY", 180, 320)
        draw_label("2 - CAPY", 400, 320)
        draw_label("3 - KITTY", 620, 320)

        pygame.display.flip()

        # Handle keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: selected = "bunny"
                elif event.key == pygame.K_2: selected = "capybara"
                elif event.key == pygame.K_3: selected = "cat"
                
                if selected:
                    pygame.display.flip()
                    pygame.time.delay(500)
                    return selected
        clock.tick(60)
    return selected

def run_level(screen, clock, player, level_data, pops_group):
    target_score = level_data['score']
    bean_speed = level_data['bean_speed']
    spawn_time = level_data['spawn_time']
    level_name = level_data['name']

    # Reset player position
    PLAYER_START_X = WIDTH // 2 - milktea_img.get_width() // 2
    player.rect.topleft = (PLAYER_START_X, HEIGHT - 220)
    
    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups_group = pygame.sprite.Group()
    bombs_group = pygame.sprite.Group()
    
    all_sprites.add(player)

    score = 0
    spawn_timer = 0
    
    # Level 3 specific setup
    player.powerup_active = False # Ensure powerup is reset

    while True:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shoot_sound.play()
                new_pearls = player.shoot(pearl_img)
                projectiles.add(new_pearls)
                all_sprites.add(new_pearls)

        # --- Update Logic ---
        all_sprites.update()
        pops_group.update() # Update pop effects
        
        # Power-up Management
        if player.powerup_active and pygame.time.get_ticks() - player.powerup_timer > 5000:
            player.powerup_active = False

        # Enemy/Item Spawning
        spawn_timer += 1
        if spawn_timer >= spawn_time:
            bean_x = random.randint(50, WIDTH - 80)
            
            # Coffee Bean always spawns
            new_bean = CoffeeBean(bean_x, -50, coffee_img, bean_speed)
            enemies.add(new_bean)
            all_sprites.add(new_bean)
            
            # Special items spawn for Level 3
            if 'survival' in level_data and level_data['survival']:
                chance = random.random()
                if chance < 0.05:
                    new_powerup = PowerUp(random.randint(50, WIDTH - 100), -80, powerup_img, bean_speed - 1)
                    powerups_group.add(new_powerup)
                    all_sprites.add(new_powerup)
                elif chance < 0.10:
                    new_bomb = Bomb(random.randint(50, WIDTH - 100), -80, bomb_img, bean_speed)
                    bombs_group.add(new_bomb)
                    all_sprites.add(new_bomb)

            spawn_timer = 0

        # --- Collision Logic ---
        
        # 🎯 Pearls hit Beans
        hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)
        score += len(hits)
        for hit_group in hits.values():
            for hit in hit_group:
                # INTEGRATED POP EFFECT
                new_pop = PopEffect(hit.rect.centerx, hit.rect.centery, pop_img)
                pops_group.add(new_pop)
                all_sprites.add(new_pop)
        
        # 💖 Pearls hit PowerUps
        powerup_hits = pygame.sprite.groupcollide(projectiles, powerups_group, True, True)
        if powerup_hits:
            player.powerup_active = True
            player.powerup_timer = pygame.time.get_ticks()
            for hit_group in powerup_hits.values():
                for hit in hit_group:
                    new_pop = PopEffect(hit.rect.centerx, hit.rect.centery, pop_img)
                    pops_group.add(new_pop)
                    all_sprites.add(new_pop)


        # 💣 Pearls hit Bombs (Game Over)
        bomb_hits = pygame.sprite.groupcollide(projectiles, bombs_group, True, True)
        if bomb_hits:
            return "GAME OVER"
        
        # --- Drawing ---
        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        pops_group.draw(screen) # Draw pops specifically to keep logic separate if needed
        
        # Score and Level display
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        level_text = font.render(level_name, True, (255, 230, 255) if level_name != "LEVEL 3" else (255, 0, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (WIDTH - 130, 10))
        if player.powerup_active:
            powerup_text = font.render("POWER-UP ACTIVE!", True, (255, 230, 255))
            screen.blit(powerup_text, (WIDTH // 2 - powerup_text.get_width() // 2, 10))

        pygame.display.flip()
        clock.tick(60)

        # --- Win Condition Check ---
        if score >= target_score:
            return "NEXT LEVEL"

# ----------------------------------------------------
# --- 4. MAIN GAME FLOW (The cleanest version) ---
# ----------------------------------------------------

# Sequence 1: Manual Screen
pygame.display.flip()
pygame.time.wait(500)
show_manual()

# Sequence 2: Character Selection
selected_char = select_character()

# 1. Initial Player & Game Setup
PLAYER_START_X = WIDTH // 2 - milktea_img.get_width() // 2
player = Player(PLAYER_START_X, HEIGHT - 220, milktea_img)
pops_group = pygame.sprite.Group() # Group for pop effects

LEVELS = [
    {'name': 'LEVEL 1', 'score': 20, 'bean_speed': 3, 'spawn_time': 60},
    {'name': 'LEVEL 2', 'score': 30, 'bean_speed': 5, 'spawn_time': 45},
    {'name': 'LEVEL 3', 'score': 30, 'bean_speed': 7, 'spawn_time': 35, 'survival': True}
]

# 2. Level Progression Loop
final_result = None
for level_index, level_data in enumerate(LEVELS):
    # Optional: Display Level Intro screen here (Level 2 Intro, Level 3 Intro)
    if level_data['name'] == "LEVEL 3":
        screen.blit(bg_img, (0, 0))
        level3_text = font_large.render("LEVEL 3 - SURVIVAL MODE!", True, (255, 0, 255))
        screen.blit(level3_text, (WIDTH // 2 - level3_text.get_width() // 2, HEIGHT // 2 - 20))
        level3_text2 = font.render("Collect strawberries for Triple Shot!", True, (255, 0, 255))
        screen.blit(level3_text2, (WIDTH // 2 - level3_text2.get_width() // 2, HEIGHT // 2 + 30))
        pygame.display.flip()
        pygame.time.delay(3000)
        
    result = run_level(screen, clock, player, level_data, pops_group)

    if result == "GAME OVER":
        final_result = "GAME OVER"
        break
    
    if result == "NEXT LEVEL":
        if level_index < len(LEVELS) - 1:
            # Mission Accomplished Screen
            screen.blit(bg_img, (0, 0))
            win_text = font_large.render(f"{level_data['name']} Accomplished!", True, (255, 255, 255))
            text2 = font.render(f"Press ENTER to continue to {LEVELS[level_index+1]['name']}!", True, (255, 255, 255))

            char_img = pygame.image.load(CHARACTERS[selected_char]).convert_alpha()
            char_img = pygame.transform.scale(char_img, (300, 300))

            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 200))
            screen.blit(char_img, (WIDTH // 2 - char_img.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 200))
            pygame.display.flip()

            # Wait for ENTER
            waiting = True
            while waiting:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                        waiting = False
                        break
        else:
            final_result = "WIN"


# 3. Final End Game Screens
if final_result == "WIN":
    yey_sound.play()
    spawn_confetti()
    end_timer = pygame.time.get_ticks()
    
    # Celebration loop
    while pygame.time.get_ticks() - end_timer < 7000:
        screen.blit(bg_img, (0, 0))
        
        # Draw confetti
        for c in confetti_particles:
            pygame.draw.circle(screen, c["color"], (int(c["x"]), int(c["y"])), c["size"])
        confetti_particles[:] = update_confetti()

        win_text = font_large.render("YOUR CHARACTER GETS THE MILKTEA!", True, (255, 255, 255))
        char_img = pygame.image.load(MISSION_CHARACTERS[selected_char]).convert_alpha()
        char_img = pygame.transform.scale(char_img, (300, 300))
        text2 = font_large.render("CONGRATULATIONS!", True, (255, 200, 255))
        
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 200))
        screen.blit(char_img, (WIDTH // 2 - char_img.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 220))

        pygame.display.flip()
        clock.tick(60)

elif final_result == "GAME OVER":
    # Game Over screen
    screen.blit(bg_img, (0, 0))
    over_text = font_large.render("GAME OVER!", True, (255, 80, 80))
    sad_text = font.render("Your character was hit by a bomb...", True, (255, 255, 255))
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(sad_text, (WIDTH // 2 - sad_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()
    pygame.time.delay(5000)

# Final exit
pygame.quit()
sys.exit() # Use sys.exit() for a clean exit