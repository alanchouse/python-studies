import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = [(100, 100)]
dx, dy = 20, 0

food = (200, 200)

score = 0
level = 1
speed = 5

font = pygame.font.Font(None, 36)

def random_food():
    return (random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT, 20))

running = True
while running:
    screen.fill((0, 0, 0))

    # Движение
    head = (snake[0][0] + dx, snake[0][1] + dy)

    # Проверка границ
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        break

    # Проверка на себя
    if head in snake:
        break

    snake.insert(0, head)

    # Еда
    if head == food:
        score += 1
        food = random_food()

        # уровень
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    # Рисуем
    for s in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*s, 20, 20))

    pygame.draw.rect(screen, (255, 0, 0), (*food, 20, 20))

    # UI
    text = font.render(f"Score: {score} Level: {level}", True, (255,255,255))
    screen.blit(text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dx, dy = 0, -20
            if event.key == pygame.K_DOWN:
                dx, dy = 0, 20
            if event.key == pygame.K_LEFT:
                dx, dy = -20, 0
            if event.key == pygame.K_RIGHT:
                dx, dy = 20, 0

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()