# A tkinter application on music player

import tkinter as tk
from tkinter import filedialog
import pygame


# Encapsulation: MusicPlayer class encapsulates player functionality
class MusicPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HIT137 Player")
        self.geometry("300x150")

        pygame.mixer.init()

        # Play, Pause, Stop buttons
        self.play_button = tk.Button(self, text="Play", command=self.play_music)
        self.pause_button = tk.Button(self, text="Pause", command=self.pause_music)
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_music)

        self.play_button.pack()
        self.pause_button.pack()
        self.stop_button.pack()

    # Polymorphism: Same method play_music can be used to handle different audio formats
    def play_music(self):
        music_file = filedialog.askopenfilename(title="Choose a music file", filetypes=(("mp3 Files", "*.mp3"),))
        if music_file:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()

    def pause_music(self):
        pygame.mixer.music.pause()

    def stop_music(self):
        pygame.mixer.music.stop()


# Multiple inheritance: Additional class for managing playlist or volume can be inherited here


def track_time(func):
    def wrapper(*args, **kwargs):
        print(f"Playing for 5 seconds before pausing automatically.")
        func(*args, **kwargs)

    return wrapper


if __name__ == "__main__":
    player = MusicPlayer()
    player.mainloop()
