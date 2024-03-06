import pygame


class Button:
    def __init__(self, screen, rect, x, y, name, image, where_to, second_rect=None):
        self.surface = image.subsurface(rect)
        self.name = name
        self.screen = screen
        self.image = image
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, rect.width, rect.height)
        self.where_to = where_to
        self.first = rect

        if second_rect:
            self.second = second_rect
            self.setting_button = True
        else:
            self.setting_button = False

    def render(self):
        self.screen.blit(self.surface, (self.x, self.y))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
