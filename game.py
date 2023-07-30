import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((900 , 650))

runnung = True
# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
background = pygame.image.load('m_1876.jpg')
mixer.music.load("background.wav")
mixer.music.play(-1)
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('ship1.png')
playerX = 420
playerY = 580
playerX_change = 0

# enemy
enemyImg = [ ]
enemyX = [ ]
enemyY = [ ]
enemyX_change = [ ]
enemyY_change = [ ]
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0 , 835))
    enemyY.append(random.randint(50 , 200))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 580
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

score_value = 0
font = pygame.font.Font('freesansbold.ttf' , 32)
textx = 10
texty = 10

over = pygame.font.Font('freesansbold.ttf' , 64)


def show_score(x , y):
    score = font.render("Score :" + str(score_value) , True , (0 , 255 , 255))
    screen.blit(score , (x , y))

def game_over():
    overtext = over.render("GAME OVER"  , True , (255 , 0 , 0))
    screen.blit(overtext,(300,250))



def player(x , y):
    screen.blit(playerImg , (x , y))


def enemy(x , y , i):
    screen.blit(enemyImg[ i ] , (x , y))


def fire_bullet(x , y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg , (x + 16 , y + 10))


def iscollision(enemyX , enemyY , bulletX , bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX , 2)) + (math.pow(enemyY - bulletY , 2)))
    if distance < 27:
        return True
    else:
        return False


while runnung:
    # colour of screen
    screen.fill((0 , 56 , 58))
    screen.blit(background , (0 , 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnung = False

        # keyboard movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    B_SOUND = mixer.Sound('laser.wav')
                    B_SOUND.play()
                    bulletX = playerX
                    fire_bullet(playerX , bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:
        playerX = 836

    for i in range(num_of_enemies):
        if enemyY[i]>500:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over()
            break



        enemyX[ i ] += enemyX_change[ i ]
        if enemyX[ i ] <= 0:
            enemyX_change[ i ] = 0.3
            enemyY[ i ] += enemyY_change[ i ]
        elif enemyX[ i ] >= 836:
            enemyX_change[ i ] = -0.3
            enemyY[ i ] += enemyY_change[ i ]

        collision = iscollision(enemyX[ i ] , enemyY[ i ] , bulletX , bulletY)
        if collision:
            e_SOUND = mixer.Sound('explosion.wav')
            e_SOUND.play()
            bulletY = 580
            bullet_state = "ready"
            score_value += 1
            enemyX[ i ] = random.randint(0 , 835)
            enemyY[ i ] = random.randint(50 , 200)
        enemy(enemyX[ i ] , enemyY[ i ] , i)
    if bulletY <= 0:
        bulletY = 650
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX , bulletY)
        bulletY -= bulletY_change

    player(playerX , playerY)
    show_score(textx , texty)
    pygame.display.update()
