import pygame
import random
import math
import sys
import os
from pygame import mixer

# Function to get the correct resource path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except Exception:
        base_path = os.path.abspath(".")  # Normal execution path
    return os.path.join(base_path, relative_path)

# Initialize Pygame
pygame.init()

# Game window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rysiu inwazja")

# Initialize audio mixer
mixer.init()

# Try to load background music
try:
    mixer.music.load(resource_path("audio.mp3"))
    mixer.music.set_volume(0.3)  # 30% volume
    mixer.music.play(-1)  # Loop indefinitely
except FileNotFoundError:
    print("Background music file not found - continuing without audio")

# Frame rate controller
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Adjusted speeds (pixels per second)
PLAYER_SPEED = 350  # Increased from 250
ENEMY_SPEED = 120
BULLET_SPEED = 700  # 1.75x of original 400 (400 * 1.75 = 700)

# Player settings
player_img = pygame.image.load(resource_path("player.png"))
player_width = 64
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - 100

# Enemy settings
enemy_img = pygame.image.load(resource_path("enemy.png"))
enemy_width = 64
enemies = []
num_enemies = 6

# Bullet settings
bullet_img = pygame.image.load(resource_path("bullet.png"))
bullet_width = 32
bullet_state = "ready"

# Score
low_taper_fady = 0
font = pygame.font.Font("freesansbold.ttf", 32)

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullet_state, bullet_x, bullet_y
    bullet_state = "fire"
    bullet_x = x
    bullet_y = y
    # Add shooting sound
    mixer.Sound(resource_path("laser.wav")).play()

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    if distance < 27:
        mixer.Sound(resource_path("explosion.wav")).play()
        return True
    return False

def show_score():
    score_text = font.render(f"Low Taper Fady: {low_taper_fady}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Initialize enemies
for i in range(num_enemies):
    enemies.append({
        "x": random.randint(0, SCREEN_WIDTH - enemy_width),
        "y": random.randint(50, 150),
        "speed": ENEMY_SPEED
    })

# Game loop variables
running = True
bullet_x = 0
bullet_y = player_y
prev_time = pygame.time.get_ticks()

while running:
    # Delta time calculation
    current_time = pygame.time.get_ticks()
    dt = (current_time - prev_time) / 1000
    prev_time = current_time
    
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                fire_bullet(player_x, player_y)
    
    # Player movement with both arrow keys and A/D
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
        player_x -= PLAYER_SPEED * dt
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < SCREEN_WIDTH - player_width:
        player_x += PLAYER_SPEED * dt
    
    # Enemy movement
    for enemy_data in enemies:
        enemy_data["x"] += enemy_data["speed"] * dt
        
        if enemy_data["x"] <= 0 or enemy_data["x"] >= SCREEN_WIDTH - enemy_width:
            enemy_data["speed"] *= -1
            enemy_data["y"] += 40
        
        if is_collision(enemy_data["x"], enemy_data["y"], bullet_x, bullet_y):
            bullet_state = "ready"
            low_taper_fady += 1
            enemy_data["x"] = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy_data["y"] = random.randint(50, 150)
        
        enemy(enemy_data["x"], enemy_data["y"])
    
    # Bullet movement
    if bullet_state == "fire":
        screen.blit(bullet_img, (bullet_x + 16, bullet_y + 10))
        bullet_y -= BULLET_SPEED * dt
        if bullet_y <= 0:
            bullet_state = "ready"
    
    player(player_x, player_y)
    show_score()
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
