import pygame

from ..enums import GameFontTypeEnum


class GameFont:
    def __init__(self, type=GameFontTypeEnum.PRIMARY, size=32, bold=False):
        self.type = type
        self.size = size
        self.bold = bold

        self.set_config()
        self.set_font()

    def set_font(self):
        self.font = pygame.font.SysFont(
            self.config["font"], size=self.size, bold=self.bold
        )

        return self.font

    def set_config(self):
        self.config = {"font": "arial", "color": "Black"}

        if self.type == GameFontTypeEnum.PRIMARY_INVERT:
            self.config["color"] = "White"

        if self.type == GameFontTypeEnum.SECONDARY:
            self.config["font"] = "courier"

        if self.type == GameFontTypeEnum.SECONDARY_INVERT:
            self.config["font"] = "courier"
            self.config["color"] = "White"

    def get_center_rect(self, text, width, height):
        return text.get_rect(center=(width / 2, height / 2))

    def render(self, text):
        return self.font.render(text, True, self.config["color"])
