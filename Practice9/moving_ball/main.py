
import pygame
from ball import Ball

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Moving Ball")

WHITE = (255, 255, 255)

ball = Ball(300, 200)

run = True
clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move(0, -20)

            elif event.key == pygame.K_DOWN:
                ball.move(0, 20)

            elif event.key == pygame.K_LEFT:
                ball.move(-20, 0)

            elif event.key == pygame.K_RIGHT:
                ball.move(20, 0)

    screen.fill(WHITE)

    ball.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
