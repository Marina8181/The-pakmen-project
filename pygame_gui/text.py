import pygame
class Text:
    def __init__(self, text, size, colour, font, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.font = font
        self._config_font()
        self._config_text()

    def _config_font(self):
        self.graphic_font = pygame.font.Font(self.font, self.size)


    def _config_text(self):
        self.graphic_text = self.graphic_font.render(self.text, True, self.colour)
        self.rect = self.graphic_text.get_rect().move(self.x, self.y)

    def get_rect(self):
        return self.rect

    def change_position(self, x, y):
        self.x = x
        self.y = y
        self._config_text()  # to update self.rect too

    def change_text(self, text):
        self.text = text
        self._config_text()

    def draw(self, display):
        display.blit(self.graphic_text, [self.x, self.y])
