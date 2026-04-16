import pygame

class Ball:
    def __init__(self):
        self.x = 250
        self.y = 250
        self.radius = 25
        self.speed = 20

    def move(self, dx, dy):
        if 0 + self.radius <= self.x + dx <= 500 - self.radius:
            self.x += dx
        if 0 + self.radius <= self.y + dy <= 500 - self.radius:
            self.y += dy

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)