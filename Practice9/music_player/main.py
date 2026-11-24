import pygame
import os
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 20)
clock = pygame.time.Clock()

# музыка
folder = os.path.dirname(__file__)

playlist = [
    os.path.join(folder, "music", "track1.wav"),
    os.path.join(folder, "music", "track2.wav")
]

player = MusicPlayer(playlist)
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()
            elif event.key == pygame.K_q:
                run = False

    screen.fill((35, 40, 55))

    title = font.render("Simple Music Player", True, (255, 255, 255))
    screen.blit(title, (170, 45))

    track_name = player.get_track_name()
    track_text = font.render("Track: " + track_name, True, (255, 220, 120))
    screen.blit(track_text, (50, 140))

    status = small_font.render("P - Play   S - Stop   N - Next", True, (255, 255, 255))
    screen.blit(status, (50, 230))
    status2 = small_font.render("B - Previous   Q - Quit", True, (255, 255, 255))
    screen.blit(status2, (50, 270))

    position = player.get_position()
    position_text = small_font.render("Position: " + str(position) + " sec", True, (180, 220, 255))
    screen.blit(position_text, (50, 320))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
