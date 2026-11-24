
import pygame


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25
        self.speed = 20

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if 25 <= new_x <= 575:
            self.x = new_x

        if 25 <= new_y <= 375:
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (self.x, self.y),
            self.radius
        )
