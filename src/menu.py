import pygame

from .enums import GameFontTypeEnum
from .utils import get_image, GameFont

from .shared import Button


class Menu:
    BACKGROUND_IMAGE = get_image("background")
    FLOOR_IMAGE = get_image("floor")

    def __init__(self, config, screen, clock):
        pygame.display.set_caption("Menu")
        pygame.mouse.set_pos(0, 0)

        self.config = config
        self.clock = clock
        self.screen = screen

        self.SCREEN_WIDTH = config["SCREEN_WIDTH"]
        self.SCREEN_HEIGHT = config["SCREEN_HEIGHT"]

        self.set_buttons()

    def run(self):
        while True:
            self.clock.tick(30)

            for event in pygame.event.get():
                event_type = self.get_event_type(event)

                if event_type == "QUIT":
                    pygame.quit()
                    quit()
                    break

            match self.get_button_pressed():
                case "PLAY":
                    self.config["page"] = "GAME"
                    break
                case "SETTINGS":
                    self.config["page"] = "SETTINGS"
                    break
                case "QUIT":
                    pygame.quit()
                    quit()
                    break

            self.check_buttons_hover()

            self.blit_background()
            self.blit_title()
            self.blit_buttons()

            pygame.display.update()

    def set_buttons(self):
        x_position = 250

        self.quit_button = Button(x=x_position, y=550, content="Sair")
        self.play_button = Button(x=x_position, y=390, content="Jogar")
        self.settings_button = Button(x=x_position, y=470, content="Configurações")

    def create_overlay(self):
        return pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def get_event_type(self, event):
        match event.type:
            case pygame.QUIT:
                return "QUIT"
            case _:
                return event.type

    def get_button_pressed(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.play_button.check_pressed(mouse_position, mouse_pressed):
            return "PLAY"

        if self.settings_button.check_pressed(mouse_position, mouse_pressed):
            return "SETTINGS"

        if self.quit_button.check_pressed(mouse_position, mouse_pressed):
            return "QUIT"

    def blit_background(self):
        overlay = self.create_overlay()
        overlay.set_alpha(150)

        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
        self.screen.blit(self.FLOOR_IMAGE, (0, self.SCREEN_HEIGHT - 70))
        self.screen.blit(overlay, (0, 0))

    def blit_title(self):
        font = GameFont(type=GameFontTypeEnum.SECONDARY_INVERT, size=52, bold=True)

        title = font.render("Flappy Bird")
        title_rect = font.get_center_rect(
            title, self.SCREEN_WIDTH, self.SCREEN_HEIGHT / 2
        )

        self.screen.blit(title, title_rect)

    def blit_buttons(self):
        self.screen.blit(self.play_button.image, self.play_button.rect)
        self.screen.blit(self.settings_button.image, self.settings_button.rect)
        self.screen.blit(self.quit_button.image, self.quit_button.rect)

    def check_buttons_hover(self):
        mouse_position = pygame.mouse.get_pos()

        self.play_button.check_hover(mouse_position)
        self.settings_button.check_hover(mouse_position)
        self.quit_button.check_hover(mouse_position)
