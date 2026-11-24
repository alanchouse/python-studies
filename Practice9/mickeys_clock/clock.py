
import pygame
import math
import time


def draw_hand(screen, center, angle, length, color, width):

    # полож рук
    x = center[0] + math.cos(math.radians(angle)) * length
    y = center[1] + math.sin(math.radians(angle)) * length

    # рисуем руку
    pygame.draw.line(
        screen, color, center, (int(x), int(y)), width
    )

    # белая перч
    glove = pygame.Surface((70, 60), pygame.SRCALPHA)

    pygame.draw.ellipse(glove, (255, 255, 255), (15, 12, 42, 38))
    pygame.draw.ellipse(glove, (25, 25, 25), (15, 12, 42, 38), 3)

    # пальцы перчатки
    pygame.draw.circle(glove, (255, 255, 255), (50, 12), 8)
    pygame.draw.circle(glove, (255, 255, 255), (56, 23), 8)
    pygame.draw.circle(glove, (255, 255, 255), (55, 35), 8)
    pygame.draw.circle(glove, (255, 255, 255), (47, 47), 8)

    # обводка перчатки
    pygame.draw.circle(glove, (25, 25, 25), (50, 12), 8, 2)
    pygame.draw.circle(glove, (25, 25, 25), (56, 23), 8, 2)
    pygame.draw.circle(glove, (25, 25, 25), (55, 35), 8, 2)
    pygame.draw.circle(glove, (25, 25, 25), (47, 47), 8, 2)

    # поворот перчатки
    rotated_glove = pygame.transform.rotate(glove, -angle)

    glove_rect = rotated_glove.get_rect(
        center=(int(x), int(y))
    )

    screen.blit(rotated_glove, glove_rect)


def draw_clock(screen):

    # центр циферблат
    center = (350, 262)

    # получ времся
    current_time = time.localtime()

    minutes = current_time.tm_min
    seconds = current_time.tm_sec

    # считаем углы
    minute_angle = (minutes * 6 + seconds * 0.1) - 90
    second_angle = seconds * 6 - 90

    # прав рук мин
    draw_hand(
        screen, center, minute_angle,
        155, (25, 25, 25), 10
    )

    # лев рука сек
    draw_hand(
        screen, center, second_angle,
        105, (210, 30, 30), 7
    )

    # центр кнопка часов
    pygame.draw.circle(screen, (25, 25, 25), center, 14)
    pygame.draw.circle(screen, (220, 35, 35), center, 6)
