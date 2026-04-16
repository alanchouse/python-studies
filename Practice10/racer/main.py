import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# Машина
car_x = 180
car_y = 500
car_speed = 5

# Монеты
coins = []
coin_count = 0

font = pygame.font.Font(None, 36)

running = True
while running:
    screen.fill((50, 50, 50))

    # Дорога
    pygame.draw.rect(screen, (100, 100, 100), (100, 0, 200, HEIGHT))

    # Машина
    pygame.draw.rect(screen, (0, 0, 255), (car_x, car_y, 40, 60))

    # Случайные монеты
    if random.randint(1, 50) == 1:
        coins.append([random.randint(120, 260), 0])

    for coin in coins:
        coin[1] += 5
        pygame.draw.circle(screen, (255, 215, 0), coin, 10)

        # Проверка столкновения
        if car_x < coin[0] < car_x + 40 and car_y < coin[1] < car_y + 60:
            coins.remove(coin)
            coin_count += 1

    # Счетчик
    text = font.render(f"Coins: {coin_count}", True, (255, 255, 255))
    screen.blit(text, (250, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 110:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < 250:
        car_x += car_speed

    pygame.display.flip()
    clock.tick(30)

pygame.quit()