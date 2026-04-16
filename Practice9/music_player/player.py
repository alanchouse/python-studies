import pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.tracks = ["music/track1.wav", "music/track2.wav"]
        self.index = 0

    def play(self):
        pygame.mixer.music.load(self.tracks[self.index])
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.index = (self.index + 1) % len(self.tracks)
        self.play()

    def prev(self):
        self.index = (self.index - 1) % len(self.tracks)
        self.play()