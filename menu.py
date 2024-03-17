import sys
from tkinter import simpledialog
from music import *
from config import *
from button import *

class Menu:
    def __init__(self, screen, image, buttons, music_playing=True, player=None):
        self.screen = screen
        self.image = image
        self.image_rect = image.get_rect()
        self.buttons = buttons
        self.next = ""
        self.music_playing = music_playing

        if player:
            self.player = player
        self.font = pygame.font.Font(None, 36)

    def run(self):
        self.next = ""

        while self.next == "":
            self.handle_events()
            self.render()
            pygame.display.flip()

        return self.next

    def render(self):
        self.screen.blit(self.image, (0, 0))

        for button in self.buttons:
            button.render()

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        if hasattr(button, 'second'):
                            temp = button.first
                            button.first = button.second
                            button.second = temp

                            button.surface = button.image.subsurface(button.first)

                            if button.name == "music":
                                if self.music_playing:
                                    set_music_playing(False)
                                    self.music_playing = False
                                else:
                                    set_music_playing(True)
                                    self.music_playing = True
                            elif button.name == "sfx":
                                if config["settings"]["sfx"] == "on":
                                    set_sfx_playing(False)
                                else:
                                    set_sfx_playing(True)

                                print(config["settings"]["sfx"])
                        else:
                            self.next = button.where_to

            elif event.type == pygame.QUIT:
                before_quit()
                sys.exit(0)


class InGameMenu(Menu):
    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        self.next = button.where_to

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next = "back"

            elif event.type == pygame.QUIT:
                sys.exit(0)


class EndMenu(Menu):

    def __init__(self, screen, image, buttons, level, score):
        super().__init__(screen, image, buttons)
        self.level = level
        self.score = score

    def run(self):
        self.render()
        pygame.display.flip()

        self.next = ""
        name = simpledialog.askstring("Input", "Your name:")
        if name is None:
            name = ""

        score_text = self.font.render("Score:    {:04d}".format(self.score), True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(480, 250))

        level = 0
        names = 0

        match self.level:
            case 0:
                level = "level1"
                names = "names1"
            case 1:
                level = "level2"
                names = "names2"
            case 2:
                level = "level3"
                names = "names3"

        if self.score > int(config[level]["1"]):

            config[level]["3"] = config[level]["2"]
            config[names]["3"] = config[names]["2"]

            config[level]["2"] = config[level]["1"]
            config[names]["2"] = config[names]["1"]

            config[level]["1"] = str(self.score)
            config[names]["1"] = name

        elif self.score > int(config[level]["2"]):

            config[level]["3"] = config[level]["2"]
            config[names]["3"] = config[names]["2"]

            config[level]["2"] = str(self.score)
            config[names]["2"] = name

        elif self.score > int(config[level]["3"]):

            config[level]["3"] = str(self.score)
            config[names]["3"] = name

        place1_text = self.font.render("#1: {}    {}".format(config[names]["1"], config[level]["1"]), True, (0, 0, 0))
        place2_text = self.font.render("#2: {}    {}".format(config[names]["2"], config[level]["2"]), True, (0, 0, 0))
        place3_text = self.font.render("#3: {}    {}".format(config[names]["3"], config[level]["3"]), True, (0, 0, 0))

        place1_rect = place1_text.get_rect(center=(480, 300))
        place2_rect = place2_text.get_rect(center=(480, 350))
        place3_rect = place3_text.get_rect(center=(480, 400))

        while self.next == "":
            self.handle_events()
            self.render()

            self.screen.blit(score_text, score_rect)
            self.screen.blit(place1_text, place1_rect)
            self.screen.blit(place2_text, place2_rect)
            self.screen.blit(place3_text, place3_rect)

            pygame.display.flip()

        return self.next

