import pygame
import os


class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.current_track = 0

    def play(self):
        if not self.playlist:
            return

        file_name = self.playlist[self.current_track]

        if os.path.exists(file_name):
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next_track(self):
        if not self.playlist:
            return

        self.current_track += 1
        if self.current_track >= len(self.playlist):
            self.current_track = 0
        self.play()

    def previous_track(self):
        if not self.playlist:
            return

        self.current_track -= 1
        if self.current_track < 0:
            self.current_track = len(self.playlist) - 1
        self.play()

    def get_track_name(self):
        if not self.playlist:
            return "No tracks"

        return os.path.basename(self.playlist[self.current_track])

    def get_position(self):
        position = pygame.mixer.music.get_pos()
        if position < 0:
            return 0
        return position // 1000
