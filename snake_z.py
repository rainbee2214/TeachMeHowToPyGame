# snake_z.py
import pygame
import random
import sys

width = 450
height = 450
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue =(0,0,255)

fps = 15 

def clamp(x, minimum, maximum):
    if x > maximum: return maximum
    if x < minimum: return minimum
    return x

def detectCollisions(x1,y1,w1,h1, x2,y2,w2,h2):
    if x1+w1>x2 and x2+w2>x1 and y1+h1>y2 and y2+h2>y1: return True
    return False

def relocateDot():
    return  round(random.uniform(0, width-playerWidth)),round(random.uniform(0, height-playerWidth))

def message_to_screen(message, x, y, color, f):
    screen_message = f.render(message, True, color)
    screen.blit(screen_message, [x-screen_message.get_width()/2.0, y-screen_message.get_height()/2.0])

pygame.init()
smallFont = pygame.font.SysFont(None, 22)
bigFont = pygame.font.SysFont(None, 60)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("snake_z")

gameOver = False
reset = True
clock = pygame.time.Clock()

playerWidth = 10
x = width/2.0
y = height/2.0

x_change = 10
y_change = 0

dot_x, dot_y = relocateDot()

topOfSnake = 0
snake = []
snake.append([clamp(x, 0, width-playerWidth), clamp(y, 0, height-playerWidth), playerWidth, playerWidth])

while not gameOver:
    clock.tick(fps)
    while reset:
        screen.fill(black)
        message_to_screen("snake_z", width/2.0, height/2.0, green, bigFont)
        message_to_screen("press space to play", width/2.0, height*0.8, green, smallFont)
        message_to_screen("press esc to quit", width/2.0, height*0.85, green, smallFont)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                gameOver = True
                reset = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset = False
                x = width/2.0
                y = height/2.0

                x_change = playerWidth
                y_change = 0
                snake = []
                snake.append([clamp(x, 0, width-playerWidth), clamp(y, 0, height-playerWidth), playerWidth, playerWidth])


        pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset = True
            if event.key == pygame.K_UP and y_change == 0:
                y_change = -playerWidth
                x_change = 0
            if event.key == pygame.K_DOWN and y_change == 0:
                y_change = playerWidth
                x_change = 0
            if event.key == pygame.K_LEFT and x_change == 0:
                x_change = -playerWidth
                y_change = 0
            if event.key == pygame.K_RIGHT and x_change == 0:
                x_change = playerWidth
                y_change = 0

    x += x_change
    y += y_change

    # checking for collisions with walls
    if x <= 0 or x >= width-playerWidth or y <= 0 or y >= height-playerWidth:
        reset = True

    dot = [dot_x, dot_y, playerWidth, playerWidth]

    snake[topOfSnake] = [clamp(x, 0, width-playerWidth), clamp(y, 0, height-playerWidth), playerWidth, playerWidth]
    
    if detectCollisions(snake[topOfSnake][0], snake[topOfSnake][1], snake[topOfSnake][2], snake[topOfSnake][3], dot[0], dot[1], dot[2], dot[3]):
        dot_x, dot_y = relocateDot()
        snake.append([x, y, playerWidth, playerWidth])
        # make snake bigger
    else:
        if len(snake) > 4:
            for i in range(0, len(snake)):
                k = (i + len(snake))%len(snake)
                if k == topOfSnake or k+1 == topOfSnake: continue
                if detectCollisions(snake[topOfSnake][0], snake[topOfSnake][1], snake[topOfSnake][2], snake[topOfSnake][3], snake[i][0], snake[i][1], snake[i][2], snake[i][3]):
                    reset = True

    topOfSnake += 1
    if topOfSnake >= len(snake): topOfSnake = 0
    
    screen.fill(black)
    pygame.draw.rect(screen, blue, dot)

    count = 0
    # pygame.draw.rect(screen, white, player)
    for piece in snake:
        color = green
        if count%3==1:
            color = red
        elif count%3==2:
            color = blue
        pygame.draw.rect(screen, color, piece)
        count += 1
    pygame.display.update()

screen.fill(black)
pygame.display.update()
pygame.quit()

