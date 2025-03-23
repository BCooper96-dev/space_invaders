import pygame
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('player.png')
playerX = 355
playerY = 490
playerX_change = 0.5  # Increased speed

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 400))
    enemyX_change.append(0.1)
    enemyY_change.append(40)

# Bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4  # Increased speed
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
over_text = pygame.font.Font('freesansbold.ttf', 64)

# Game state
game_started = False
game_over = False

# Start Button
start_button_rect = pygame.Rect(350, 300, 100, 50)
start_button_color = (0, 255, 0)

# Leaderboard
leaderboard = []


def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render("GAME OVER!", True, (0, 245, 0))
    screen.blit(over_text, (290, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


def draw_start_button():
    pygame.draw.rect(screen, start_button_color, start_button_rect)
    start_text = font.render("Start", True, (0, 0, 0))
    screen.blit(start_text, (375, 315))


def draw_leaderboard():
    y_offset = 100
    leaderboard_text = font.render("Leaderboard", True, (255, 255, 255))
    screen.blit(leaderboard_text, (300, y_offset))
    y_offset += 40
    leaderboard_sorted = sorted(leaderboard, reverse=True) # Sort the leaderboard
    for i, score in enumerate(leaderboard_sorted):
        score_text = font.render(f"{i + 1}. {score}", True, (255, 255, 255))
        screen.blit(score_text, (300, y_offset))
        y_offset += 30


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))

    if not game_started:
        draw_start_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    game_started = True
    else:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        if playerX >= 736:
            playerX = 736

        game_over = False

        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                game_over = True
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.1
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.1

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 800)
                enemyY[i] = random.randint(50, 400)
            enemy(enemyX[i], enemyY[i], i)

        if game_over:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            leaderboard.append(score_value)
            game_started = False #restart the game
            score_value = 0 #reset the score.
            draw_leaderboard()

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

    pygame.display.update()