
import pygame
import os
from clock import draw_clock

pygame.init()

WIDTH = 700
HEIGHT = 525

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

# Загруз фото микки
image_path = os.path.join(
    os.path.dirname(__file__),
    "images",
    "reference_clock.jpeg"
)

background = pygame.image.load(image_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # картинкарук
    screen.blit(background, (0, 0))

    # движ руки
    draw_clock(screen)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
