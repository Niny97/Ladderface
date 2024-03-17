from game import *
from menu import *
from button import *
import os
from music import *
from config import *


BLACK = (0, 0, 0)

buttons = pygame.image.load("buttons.png")

button_rects = {
    0: pygame.Rect(0, 374, 328, 80),     # play
    1: pygame.Rect(331, 374, 328, 80),   # settings
    2: pygame.Rect(0, 456, 328, 80),     # about
    3: pygame.Rect(331, 456, 328, 80),   # exit
    4: pygame.Rect(0, 0, 191, 191),      # level1
    5: pygame.Rect(191, 0, 190, 191),    # level2
    6: pygame.Rect(380, 0, 191, 191),    # level3
    7: pygame.Rect(440, 282, 218, 88),   # back
    8: pygame.Rect(0, 191, 218, 88),     # try again
    9: pygame.Rect(218, 191, 218, 88),   # to menu
    10: pygame.Rect(0, 282, 218, 88),    # resume
    11: pygame.Rect(219, 282, 218, 88),  # restart
    12: pygame.Rect(449, 201, 70, 67),   # setting off
    13: pygame.Rect(535, 201, 70, 67)    # setting on
}

objects = pygame.image.load("stuff.png")

obj_rects = {
    0: pygame.Rect(142, 0, 102, 127),    # blue monster
    1: pygame.Rect(16, 0, 102, 127),     # yellow
    2: pygame.Rect(29, 152, 78, 206),    # player
    5: pygame.Rect(128, 128, 128, 128),  # crystal
    6: pygame.Rect(128, 256, 128, 128),  # full heart
    7: pygame.Rect(256, 256, 128, 128),  # empty heart
    8: pygame.Rect(314, 252, 327, 78),   # resume
    9: pygame.Rect(315, 356, 327, 78),   # restart
    10: pygame.Rect(317, 458, 327, 78),  # to menu
}


config_file_path = 'config.ini'
if os.path.exists(config_file_path):
    config.read('config.ini')

menu_image = pygame.image.load("menu.png")
background_image = pygame.image.load("background.png")
settings_image = pygame.image.load("settings.png")

if config["settings"]["music"] == "on":
    playing = True
else:
    playing = False

screen = pygame.display.set_mode([960, 640])
game = Game(screen, objects, obj_rects, buttons, button_rects)


# Main menu
play_button = Button(screen, button_rects[0], 315, 211, "play", buttons, "levels")
settings_button = Button(screen, button_rects[1], 315, 306, "settings", buttons, "settings")
about_button = Button(screen, button_rects[2], 315, 401, "about", buttons, "about")
exit_button = Button(screen, button_rects[3], 315, 496, "exit", buttons, "exit")
menu = Menu(screen, menu_image, [play_button, settings_button, about_button, exit_button])

# Level menu
level1_button = Button(screen, button_rects[4], 138, 208, "level1", buttons, "level1")
level2_button = Button(screen, button_rects[5], 383, 208, "level2", buttons, "level2")
level3_button = Button(screen, button_rects[6], 628, 208, "level3", buttons, "level3")
back_button = Button(screen, button_rects[7], 370, 470, "back", buttons, "menu")
levels_menu = Menu(screen, background_image, [level1_button, level2_button, level3_button, back_button])
levels = ["level1", "level2", "level3"]

# About menu
about_image = pygame.image.load("about.png")
about_menu = Menu(screen, about_image, [back_button])


pygame.mixer.music.load("mixkit-music.mp3")
pygame.mixer.music.play(-1)

music_first = 13
music_second = 12

sfx_first = 13
sfx_second = 12

# Check previously saved music and sfx settings
if config["settings"]["music"] == "off":
    pygame.mixer.music.pause()
    music_first = 12
    music_second = 13
elif config["settings"]["sfx"] == "off":
    sfx_first = 12
    sfx_second = 13


# Settings menu
music_button = Button(screen, button_rects[music_first], 610, 175, "music", buttons, "settings", button_rects[music_second])
sfx_button = Button(screen, button_rects[sfx_first], 610, 305, "sfx", buttons, "settings", button_rects[sfx_second])
settings_menu = Menu(screen, settings_image, [back_button, music_button, sfx_button], music_playing=playing)


where = "menu"

while True:
    match where:

        case "menu":
            game.restart()
            where = menu.run()
        case "levels":
            where = levels_menu.run()
        case "settings":
            where = settings_menu.run()
        case "about":
            where = about_menu.run()
        case "level1":
            game.lvl = 0
            where = game.run()
        case "level2":
            game.lvl = 1
            where = game.run()
        case "level3":
            game.lvl = 2
            where = game.run()
        case "restart":
            game.restart()
            where = levels[game.lvl]
        case "exit":
            before_quit()
            pygame.quit()
            sys.exit(0)

