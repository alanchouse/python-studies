import pygame
import datetime
import math

class MickeyClock:
    def __init__(self):
        self.center = (250, 250)

    def draw_hand(self, screen, angle, length, color):
        x = self.center[0] + length * math.sin(math.radians(angle))
        y = self.center[1] - length * math.cos(math.radians(angle))
        pygame.draw.line(screen, color, self.center, (x, y), 5)

    def draw(self, screen):
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        minute_angle = minutes * 6
        second_angle = seconds * 6

        self.draw_hand(screen, minute_angle, 100, (0, 0, 0))
        self.draw_hand(screen, second_angle, 150, (255, 0, 0))