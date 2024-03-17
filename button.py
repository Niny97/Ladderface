import pygame


class Button:
    def __init__(self, screen, image_rect, x, y, name, image, where_to, image_second_rect=None):
        self.surface = image.subsurface(image_rect)
        self.name = name
        self.screen = screen
        self.image = image
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, image_rect.width, image_rect.height)
        self.where_to = where_to
        self.first = image_rect

        if image_second_rect:
            self.second = image_second_rect

    def render(self):
        self.screen.blit(self.surface, (self.x, self.y))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
