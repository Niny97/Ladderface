import pygame
from config import *

pygame.mixer.init()


def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)  # -1 makes the music loop


def set_music_playing(playing):
    if playing:
        pygame.mixer.music.unpause()
        config["settings"]["music"] = "on"

    else:
        pygame.mixer.music.pause()
        config["settings"]["music"] = "off"

def set_sfx_playing(playing):
    if playing:
        config["settings"]["sfx"] = "on"

    else:
        config["settings"]["sfx"] = "off"
