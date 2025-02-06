import pygame

from ..enums import GameFontTypeEnum, ButtonTypeEnum, ButtonSizeEnum
from ..utils import GameFont


class Button:
    def __init__(
        self,
        x,
        y,
        content,
        type=ButtonTypeEnum.PRIMARY,
        size=ButtonSizeEnum.MEDIUM,
    ):
        self.type = type
        self.size = size

        self.set_config()

        self.is_hover = False
        self.is_pressed = False

        self.x = x
        self.y = y
        self.content = content
        self.width = self.config["width"]
        self.height = self.config["height"]
        self.fontsize = self.config["fontsize"]

        self.set_content()
        self.set_button_image()

        self.blit_button()

    def set_config(self):
        self.config = {
            "width": 300,
            "height": 50,
            "fontsize": 28,
            "color": "White",
            "font": GameFontTypeEnum.PRIMARY,
        }

        if self.type == ButtonTypeEnum.SECONDARY:
            self.config["color"] = "Black"
            self.config["font"] = GameFontTypeEnum.PRIMARY_INVERT

        if self.size == ButtonSizeEnum.SMALL:
            self.config["width"] = 200
            self.config["height"] = 40
            self.config["fontsize"] = 26

        if self.size == ButtonSizeEnum.LARGE:
            self.config["width"] = 400
            self.config["height"] = 60
            self.config["fontsize"] = 40

    def set_button_image(self):
        self.image = self.create_overlay()
        self.image.fill(self.config["color"])
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def set_content(self):
        self.font = GameFont(type=self.config["font"], size=self.fontsize)

        self.text = self.font.render(self.content)
        self.text_rect = self.font.get_center_rect(self.text, self.width, self.height)

    def create_overlay(self):
        return pygame.Surface((self.width, self.height))

    def blit_button(self):
        self.image.blit(self.text, self.text_rect)
        self.original_image = self.image.copy()

    def check_pressed(self, position, pressed, force_update=False):
        mouse_pressed = self.rect.collidepoint(position) and pressed[0]

        if self.is_pressed and mouse_pressed and not force_update:
            return False

        self.is_pressed = mouse_pressed

        if self.is_pressed:
            overlay = self.create_overlay()
            overlay.set_alpha(80)
            self.image.blit(overlay, (0, 0))
        else:
            self.check_hover(position, force_update=True)

        return self.is_pressed

    def check_hover(self, position, force_update=False):
        mouse_hover = self.rect.collidepoint(position)

        if self.is_hover and mouse_hover and not force_update:
            return True

        self.is_hover = mouse_hover

        if self.is_hover:
            overlay = self.create_overlay()
            overlay.set_alpha(50)
            self.image = self.original_image.copy()
            self.image.blit(overlay, (0, 0))
        else:
            self.image = self.original_image.copy()

        return self.is_hover
