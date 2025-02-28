import pygame

from .enums import GameFontTypeEnum
from .utils import GameFont
from .shared import Select


class SettingSection:
    def __init__(self, y, text, config, screen, current_option, options):
        self.font = GameFont(type=GameFontTypeEnum.SECONDARY_INVERT, size=26, bold=True)

        self.y = y
        self.text = text
        self.screen = screen
        self.options = options
        self.current_option = current_option

        self.height = 120
        self.width = 0.9 * config["SCREEN_WIDTH"]
        self.SCREEN_WIDTH = config["SCREEN_WIDTH"]

        self.set_image()
        self.set_content()
        self.set_select()
        self.blit_content()
        self.blit_border()

    def set_image(self):
        self.image = self.create_overlay()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(center=(self.SCREEN_WIDTH / 2, self.y))

    def set_content(self):
        self.text = self.font.render(self.text)
        self.text_rect = self.font.get_center_rect(
            self.text, self.text.get_width(), self.height
        )

    def set_select(self):
        select_width = 225
        select_height = 46

        self.select = Select(
            screen=self.screen,
            width=select_width,
            values=self.options,
            initial_value=self.current_option,
            y=(self.y - select_height / 2),
            x=self.rect.x + self.width - select_width,
        )

    def create_overlay(self, width=None, height=None):
        overlay_width = width or self.width
        overlay_height = height or self.height

        return pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)

    def blit_content(self):
        self.image.blit(self.text, self.text_rect)

    def blit_border(self):
        width = 4
        color = (255, 255, 255, 150)
        start_line = (0, self.height)
        end_line = (self.width, self.height)

        pygame.draw.line(
            self.image,
            color,
            start_line,
            end_line,
            width,
        )

    def render(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.render()
        self.select.update()
        self.select.render()

    def get_value(self):
        return self.select.value
