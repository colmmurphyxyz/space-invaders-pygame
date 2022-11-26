import sys
import pygame

pygame.init()

size = width, height = 640, 480
black = (0, 0, 0)

screen = pygame.display.set_mode(size)

ship = pygame.image.load("sprite_ship.png")
shippos = 160
shipchange = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shipchange -= 1
            if event.key == pygame.K_RIGHT:
                shipchange += 1
        if event.type == pygame.KEYUP:
            shipchange = 0

    if shippos + shipchange in range(0, width - ship.get_width()):
        shippos += shipchange
        screen.fill(black)
        screen.blit(ship, (shippos, height - ship.get_height() - 10))

    pygame.display.flip()

