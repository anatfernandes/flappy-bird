import pygame

from .enums import GameFontTypeEnum
from .utils import get_image, GameFont
from .shared import Button

from .setting_section import SettingSection


class Settings:
    BACKGROUND_IMAGE = get_image("background")
    FLOOR_IMAGE = get_image("floor")

    def __init__(self, config, screen, clock):
        pygame.display.set_caption("Configurações")
        pygame.mouse.set_pos(0, 0)

        self.config = config
        self.clock = clock
        self.screen = screen

        self.SCREEN_WIDTH = config["SCREEN_WIDTH"]
        self.SCREEN_HEIGHT = config["SCREEN_HEIGHT"]

        self.set_buttons()
        self.set_sections()

    def run(self):
        while True:
            self.clock.tick(30)

            for event in pygame.event.get():
                event_type = self.get_event_type(event)

                if event_type == "QUIT":
                    pygame.quit()
                    quit()
                    break

            match self.check_button_pressed():
                case "MENU":
                    self.config["page"] = "MENU"
                    break

            self.blit_screen()

            self.difficulty_section.update()
            self.mode_section.update()

            self.handle_update_config()

            pygame.display.update()

    def set_buttons(self):
        x_position = 250
        y_position = self.SCREEN_HEIGHT - 70

        self.menu_button = Button(x=x_position, y=y_position, content="Menu")

    def set_sections(self):
        config_values = self.get_config_values()

        self.difficulty_section = SettingSection(
            y=200,
            text="Dificuldade",
            config=self.config,
            screen=self.screen,
            options=config_values["difficulties"],
            current_option=config_values["current_difficulty"],
        )

        self.mode_section = SettingSection(
            y=320,
            text="Modo",
            config=self.config,
            screen=self.screen,
            options=config_values["modes"],
            current_option=config_values["current_mode"],
        )

    def create_overlay(self):
        return pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def blit_background(self):
        overlay = self.create_overlay()
        overlay.set_alpha(150)

        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
        self.screen.blit(self.FLOOR_IMAGE, (0, self.SCREEN_HEIGHT - 70))
        self.screen.blit(overlay, (0, 0))

    def blit_title(self):
        font = GameFont(type=GameFontTypeEnum.SECONDARY_INVERT, size=46, bold=True)

        title = font.render("Configurações")
        title_rect = font.get_center_rect(title, self.SCREEN_WIDTH, 100)

        self.screen.blit(title, title_rect)

    def blit_buttons(self):
        self.screen.blit(self.menu_button.image, self.menu_button.rect)

    def blit_screen(self):
        self.blit_background()
        self.blit_title()
        self.blit_buttons()

    def check_button_pressed(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.menu_button.check_pressed(mouse_position, mouse_pressed):
            return "MENU"

    def update_config(self, value, setting):
        update = self.config[setting]["current"] != value

        if update:
            self.config[setting]["current"] = value

    def handle_update_config(self):
        self.update_config(self.difficulty_section.get_value(), "difficulties")
        self.update_config(self.mode_section.get_value(), "modes")

    def get_event_type(self, event):
        match event.type:
            case pygame.QUIT:
                return "QUIT"
            case _:
                return event.type

    def get_config_values(self):
        modes = list(self.config["modes"].keys())
        difficulties = list(self.config["difficulties"].keys())

        difficulties.remove("current")
        modes.remove("current")

        return {
            "modes": modes,
            "difficulties": difficulties,
            "current_mode": self.config["modes"]["current"],
            "current_difficulty": self.config["difficulties"]["current"],
        }
