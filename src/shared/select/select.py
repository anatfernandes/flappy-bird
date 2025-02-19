import pygame

from ...enums import GameFontTypeEnum
from ...utils import GameFont

from .button import SelectButton


class Select:
    def __init__(self, screen, x, y, width, initial_value, values):
        self.font = GameFont(type=GameFontTypeEnum.SECONDARY, size=24)

        self.screen = screen

        self.x = x
        self.y = y
        self.width = width
        self.values = values
        self.value = initial_value
        self.value_index = self.get_value_index(self.value)

        self.set_buttons()
        self.set_height()
        self.set_image()
        self.set_content()

    def set_buttons(self):
        self.back_button = SelectButton(x=self.x, y=self.y, content="<")

        self.next_button = SelectButton(
            x=self.x + self.width - self.back_button.width, y=self.y, content=">"
        )

    def set_height(self):
        self.height = self.back_button.height

    def set_image(self):
        self.image = self.create_overlay()
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def set_content(self):
        self.text = self.font.render(self.value)
        self.text_rect = self.font.get_center_rect(self.text, self.width, self.height)

    def create_overlay(self):
        return pygame.Surface((self.width, self.height))

    def get_value_index(self, value):
        return self.values.index(value)

    def blit_content(self):
        self.image.blit(self.text, self.text_rect)

    def blit_buttons(self):
        self.image.blit(self.back_button.image, (0, 0))
        self.image.blit(
            self.next_button.image, (self.image.get_width() - self.next_button.width, 0)
        )

    def update_value(self, value):
        values_size = len(self.values)
        index = value + self.value_index
        new_index = index % values_size

        self.value = self.values[new_index]
        self.value_index = self.get_value_index(self.value)

    def check_button_pressed(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.back_button.check_pressed(mouse_position, mouse_pressed):
            return self.update_value(-1)

        if self.next_button.check_pressed(mouse_position, mouse_pressed):
            return self.update_value(1)

    def update(self):
        self.check_button_pressed()

    def render(self):
        self.set_image()
        self.set_content()
        self.blit_content()
        self.blit_buttons()

        self.screen.blit(self.image, self.rect)
