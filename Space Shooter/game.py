import pygame
import random
import math
from pygame import mixer

# Pygame Intializaation
pygame.init()

# Making the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
player_X = 370
player_Y = 480
player_X_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# List of Enemies
enemyImg = []
enemy_X = []
enemy_Y = []
enemy_X_change = []
enemy_Y_change = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemy_X.append(random.randint(0, 736))
    enemy_Y.append(random.randint(50, 150))
    enemy_X_change.append(2)
    enemy_Y_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is moving

bulletImg = pygame.image.load("bullet.png")
bullet_X = 0
bullet_Y = 480
bullet_X_change = 0
bullet_Y_change = 20
bullet_state = "ready"  

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Collision Function
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
    
# Score
score_value = 0    
font = pygame.font.Font("freesansbold.ttf", 32)

text_X = 10
text_Y = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text():
    game_over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))



# Game Loop
running = True

while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystoke is pressed check whether its right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player_X_change = -5
        if event.key == pygame.K_RIGHT:
            player_X_change = 5
        if event.key == pygame.K_UP:
            if bullet_state == "ready":
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                # Get the current X coordinate of spaceship
                bullet_X = player_X
                fire_bullet(bullet_X, bullet_Y)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            player_X_change = 0
  
    # Checking the boundries of spaceship so it doesn't go out of bounds
    player_X += player_X_change

    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736
    
    player(player_X, player_Y)

    # Enemies Movement
    for i in range(num_of_enemies):

        if enemy_Y[i] > 430:
            for j in range(num_of_enemies):
                enemy_Y[j] = 2000
            game_over_text()
            break

        enemy_X[i] += enemy_X_change[i]

        if enemy_X[i] <= 0:
            enemy_X_change[i] = 2
            enemy_Y[i] += enemy_Y_change[i]
        elif enemy_X[i] >= 736:
            enemy_X_change[i] = -2
            enemy_Y[i] += enemy_Y_change[i]
        
        enemy(enemy_X[i], enemy_Y[i], i)

        # Collision
        collision = isCollision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_Y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_X[i] = random.randint(0, 736)
            enemy_Y[i] = random.randint(50, 150)

    # Bullet Movement
    if bullet_Y <= 0:
        bullet_Y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Y_change
    
    show_score(text_X, text_Y)

    pygame.display.update()