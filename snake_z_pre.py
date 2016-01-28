import pygame
import sys
import time
import random
from pygame import *

width = 450
height = 450
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

playerWidth = 10
highScore = 0

pygame.init()
smallFont = pygame.font.SysFont(None, 25) # 25 = font size
bigFont = pygame.font.SysFont(None, 65) # 25 = font size

def clamp(n, min, max):
    if (n < min): return min
    if ( n > max): return max
    return n

def relocateDot():
    return round(random.uniform(0, width-playerWidth*dotSize)),round(random.uniform(0, height-playerWidth*dotSize))

def detectCollisions(x1, y1, w1, h1, x2, y2, w2, h2):
    if x1+w1>x2 and x2+w2>x1 and y1+h1>y2 and h2+y2>y1:return True
    else:return False

def message_to_screen(message, x, y, color, f):
    screen_message_text = f.render(message, True, color)
    screen.blit(screen_message_text, [x-screen_message_text.get_width()/2.0,y-screen_message_text.get_height()/2.0])

backgroundColour = white

fps = 23
# speed = 1
dotSize = 0.75

screen = pygame.display.set_mode((width,height)) # return a pygame.surface object
pygame.display.set_caption("snake_z")

gameExit = False
reset = True

clock = pygame.time.Clock()

x = width/2
y = height/2

x_change = playerWidth
y_change = 0

randomDotX,randomDotY =  relocateDot()
player = [clamp(x, 0, width-playerWidth), clamp(y, 0, height-playerWidth), playerWidth, playerWidth]
 
snake = []
snake.append([x,y, playerWidth, playerWidth])

topOfSnake = 0
delta = 2
endGameMessage = ""
while not gameExit:
    clock.tick(fps)

    while reset:
        screen.fill(backgroundColour)
        randomDotX,randomDotY =  relocateDot()

        message_to_screen(endGameMessage, width*0.5, height*0.35, black, smallFont)
        message_to_screen("snake_z", width*0.5, height*0.5, black, bigFont)
        message_to_screen("high score: " + str(highScore), width*0.5, height*0.65, black, smallFont)
        message_to_screen("press space to play", width*0.5, height*0.8, black, smallFont)
        message_to_screen("press esc to quit", width*0.5, height*0.85, black, smallFont)
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                gameExit = True
                reset = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                x = width/2
                y = height/2

                x_change = playerWidth
                y_change = 0

                reset = False
                # reset the snake
                x = width/2
                y = height/2
                sizeOfSnake = 1 
                topOfSnake = 0
                snake = []
                snake.append([x,y, playerWidth, playerWidth])
                endGameMessage = ""

    for event in pygame.event.get():
        # print event
        if event.type == QUIT: gameExit = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            reset = True
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT and x_change == 0:
              y_change = 0
              x_change = -playerWidth
          elif event.key == pygame.K_RIGHT and x_change == 0:
              y_change = 0
              x_change = playerWidth
          elif event.key == pygame.K_UP and y_change == 0:
              x_change = 0
              y_change = -playerWidth
          elif event.key == pygame.K_DOWN and y_change == 0:
              x_change = 0
              y_change = playerWidth

    screen.fill(backgroundColour)

    # make a dot appear
    dot = [randomDotX, randomDotY, playerWidth*dotSize, playerWidth*dotSize]
    pygame.draw.rect(screen, blue, dot)

    # move player around
    x += x_change
    y += y_change

    # check for hitting edge - if so, game over
    if (x <= 0 or x >= width or y <= 0 or y >= height) and not reset:
        if (len(snake)-1)*100 > highScore:  highScore = str((len(snake)-1)*100)
        reset = True
        endGameMessage = "You hit the death wall."


    snake[topOfSnake] = [clamp(x, 0, width-playerWidth), clamp(y, 0, height-playerWidth), playerWidth, playerWidth]
    count = 0
    for piece in snake:
        if count%2==0:
            pygame.draw.rect(screen, red, piece)
        else:
            pygame.draw.rect(screen, green, piece)
        count += 1

    # if colliding with a dot,make the snake bigger and generate a new dot
    # else check for collisions with yourself (if you're bigger than 4)
    if detectCollisions(snake[topOfSnake][0], snake[topOfSnake][1], snake[topOfSnake][2], snake[topOfSnake][3], dot[0], dot[1], dot[2], dot[3]):
        randomDotX,randomDotY =  relocateDot()
        snake.append([x,y, playerWidth, playerWidth])
    else:
        if len(snake) > 4:
            for i in range(0, len(snake)):
                k = (i+ len(snake))%len(snake)
                if k == topOfSnake or k+1 == topOfSnake: continue
                if detectCollisions(snake[topOfSnake][0], snake[topOfSnake][1], snake[topOfSnake][2]-delta, snake[topOfSnake][3]-delta, snake[k][0], snake[k][1], snake[k][2]-delta, snake[k][3]-delta):
                    # print 'Collision with self: '
                    endGameMessage = "You ran into yourself. Good job."

                    reset = True

    topOfSnake += 1
    if (topOfSnake >= len(snake)): topOfSnake = 0

    message_to_screen("Score: " + str((len(snake)-1)*100), width*0.5, 20, black, smallFont)

    pygame.display.update()

screen.fill(backgroundColour)
message_to_screen("You suck", width*0.5, height*0.75, black, smallFont)
pygame.display.update()
pygame.time.wait(2)
pygame.quit()
quit()



