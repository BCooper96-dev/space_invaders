import pygame
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()

start_button_rect = pygame.Rect(0, 0, 0, 0)
leaderboard_button_rect = pygame.Rect(0, 0, 0, 0)
play_again_rect = pygame.Rect(0, 0, 0, 0) # Initialize play_again_rect

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('player.png')
playerX = 355
playerY = 490
playerX_change = 0  # Increased speed

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
enemy_speed_base = 0.1
enemy_speed_increase = 0.00005
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 75)) # Further adjusted to spawn higher.
    enemyX_change.append(enemy_speed_base)
    enemyY_change.append(40)

# Bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
over_text = pygame.font.Font('freesansbold.ttf', 64)

# Game state
game_started = True
game_over = False
show_leaderboard = False
play_again = False

# Leaderboard
leaderboard = []

# Initialize button rectangles outside the loop
start_button_rect = pygame.Rect(0, 0, 0, 0)
leaderboard_button_rect = pygame.Rect(0, 0, 0, 0)
play_again_rect = pygame.Rect(0, 0, 0, 0)  # Initialize play_again_rect

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
    start_text = font.render("Start", True, (0, 0, 0))
    text_rect = start_text.get_rect()
    button_width = text_rect.width + 40
    button_height = text_rect.height + 20
    button_x = 800 // 2 - button_width // 2
    button_y = 600 // 2 - button_height // 2 - 30
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, (0, 255, 0), button_rect)
    screen.blit(start_text, start_text.get_rect(center=button_rect.center))
    return button_rect

def draw_leaderboard_button():
    leaderboard_text = font.render("Leaderboard", True, (0, 0, 0))
    text_rect = leaderboard_text.get_rect()
    button_width = text_rect.width + 40
    button_height = text_rect.height + 20
    button_x = 800 // 2 - button_width // 2
    button_y = 600 // 2 - button_height // 2 + 30
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, (0, 0, 255), button_rect)
    screen.blit(leaderboard_text, leaderboard_text.get_rect(center=button_rect.center))
    return button_rect

def draw_leaderboard():
    y_offset = 100
    leaderboard_text = font.render("Leaderboard", True, (255, 255, 255))
    screen.blit(leaderboard_text, (300, y_offset))
    y_offset += 40
    leaderboard_sorted = sorted(leaderboard, reverse=True)
    for i, score in enumerate(leaderboard_sorted):
        score_text = font.render(f"{i + 1}. {score}", True, (255, 255, 255))
        screen.blit(score_text, (300, y_offset))
        y_offset += 30

def draw_title():
    title_font = pygame.font.Font('freesansbold.ttf', 64)
    title_text = title_font.render("Space Invaders", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(800 // 2, 600 // 4))
    screen.blit(title_text, title_rect)

def draw_play_again_button():
    play_again_text = font.render("Play Again", True, (0, 0, 0))
    text_rect = play_again_text.get_rect()
    button_width = text_rect.width + 40
    button_height = text_rect.height + 20
    button_x = 800 // 2 - button_width // 2
    button_y = 600 // 2 + 100  # Position below the game over text.
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, (255, 0, 0), button_rect)
    screen.blit(play_again_text, play_again_text.get_rect(center=button_rect.center))
    return button_rect

def game_over_text(score): # Pass the score to the game over function.
    over_text = font.render("GAME OVER!", True, (255, 0, 0))
    score_text = font.render(f"Your Score: {score}", True, (255, 0, 0)) #score text.
    screen.blit(over_text, (290, 250))
    screen.blit(score_text, (310, 300)) #draw score text.


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))

    if not game_started and not show_leaderboard:
        draw_title()
        start_button_rect = draw_start_button()
        leaderboard_button_rect = draw_leaderboard_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    game_started = True
                if leaderboard_button_rect.collidepoint(event.pos):
                    show_leaderboard = True

    elif show_leaderboard:
        draw_leaderboard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_leaderboard = False

    else:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -1.5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 1.5
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
                enemyX_change[i] = enemy_speed_base
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -enemy_speed_base
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 75)
            enemy(enemyX[i], enemyY[i], i)
            enemy_speed_base += 0.00001
            for j in range(num_of_enemies):
                if enemyX_change[j] > 0:
                    enemyX_change[j] = enemy_speed_base
                else:
                    enemyX_change[j] = -enemy_speed_base

        if game_over:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(score_value)
            play_again_rect = draw_play_again_button()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_rect.collidepoint(event.pos):
                        game_over = False
                        game_started = True
                        score_value = 0
                        enemy_speed_base = 0.1
                        for k in range(num_of_enemies):
                            enemyX[k] = random.randint(0, 736)
                            enemyY[k] = random.randint(50, 75)
                        playerX = 355
                        playerY = 490

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

    pygame.display.update()