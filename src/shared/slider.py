import pygame


class Slider:
    def __init__(
        self,
        screen,
        x,
        y,
        width,
        min,
        max,
        initial_value,
        height=15,
    ):
        self.screen = screen

        self.width = width
        self.height = height
        self.initial_value = initial_value
        self.button_height = height + 10
        self.button_middle_height = self.button_height / 2

        self.left_position = x - (width // 2)
        self.right_position = x + (width // 2)
        self.top_position = y - (height // 2)
        self.button_top_position = y - (self.button_height // 2)

        self.min = min
        self.max = max

        self.set_rects()

    def set_rects(self):
        self.background_rect = pygame.Rect(
            self.left_position, self.top_position, self.width, self.height
        )

        self.button_rect = pygame.Rect(
            self.get_initial_value(),
            self.button_top_position,
            self.button_height,
            self.button_height,
        )

    def render(self):
        pygame.draw.rect(self.screen, "black", self.background_rect, border_radius=50)
        pygame.draw.rect(self.screen, "white", self.button_rect, border_radius=50)

    def move(self, mouse_position):
        value_range = self.right_position - self.left_position
        self.button_rect.centerx = mouse_position[0]

        self.value = self.get_value()

        self.button_rect.centerx = self.left_position + (
            (value_range / (self.max - 1)) * (self.value - 1)
        )

    def get_initial_value(self):
        value_range = self.right_position - self.left_position

        return (
            self.left_position
            + ((value_range / (self.max - 1)) * (self.initial_value - 1))
            - self.button_middle_height
        )

    def get_value(self):
        value_range = self.right_position - self.left_position
        button_value = self.button_rect.centerx - self.left_position

        return int(((button_value / value_range) * (self.max)) + self.min)
