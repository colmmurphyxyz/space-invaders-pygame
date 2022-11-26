import sys
import pygame

pygame.init()

size = width, height = 640, 480
black = (0, 0, 0)

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballpos = 160
ballchange = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ballchange -= 1
            if event.key == pygame.K_RIGHT:
                ballchange += 1
        if event.type == pygame.KEYUP:
            ballchange = 0

    if ballpos + ballchange in range(0, width - 100):
        ballpos += ballchange
        screen.fill(black)
        screen.blit(ball, (ballpos, 120))

    pygame.display.flip()

