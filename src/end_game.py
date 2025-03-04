import pygame

from .enums import GameFontTypeEnum
from .utils import get_image, GameFont
from .shared import Button


class EndGame:
    BACKGROUND_IMAGE = get_image("background")
    FLOOR_IMAGE = get_image("floor")

    def __init__(self, config, screen, clock):
        pygame.display.set_caption("Fim de jogo")
        pygame.mouse.set_pos(0, 0)

        self.title_font = GameFont(
            type=GameFontTypeEnum.SECONDARY_INVERT, size=46, bold=True
        )
        self.font = GameFont(type=GameFontTypeEnum.SECONDARY_INVERT, size=32)

        self.clock = clock
        self.config = config
        self.screen = screen

        self.SCREEN_WIDTH = config["SCREEN_WIDTH"]
        self.SCREEN_HEIGHT = config["SCREEN_HEIGHT"]
        self.ai_training_mode = config["modes"]["current"] == "IA"

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

            match self.check_button_pressed():
                case "MENU":
                    self.config["page"] = "MENU"
                    break
                case "GAME":
                    self.config["page"] = "GAME"
                    break

            self.blit_screen()

            pygame.display.update()

    def set_buttons(self):
        x_position = 250
        y_position = self.SCREEN_HEIGHT - 140

        self.play_button = Button(x=x_position, y=y_position - 70, content="Reiniciar")
        self.menu_button = Button(x=x_position, y=y_position, content="Menu")

    def create_overlay(self):
        return pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def blit_background(self):
        overlay = self.create_overlay()
        overlay.set_alpha(170)

        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
        self.screen.blit(self.FLOOR_IMAGE, (0, self.SCREEN_HEIGHT - 70))
        self.screen.blit(overlay, (0, 0))

    def blit_title(self):
        title = self.title_font.render("Fim de jogo!")
        title_rect = self.title_font.get_center_rect(
            title, self.SCREEN_WIDTH, self.SCREEN_HEIGHT / 2
        )

        self.screen.blit(title, title_rect)

    def blit_content(self):
        points = self.font.render(f'Pontuação: {self.config["game"]["points"]}')
        time = self.font.render(f'Tempo: {self.config["game"]["time"]}s')
        generation = self.font.render(f'Geração: {self.config["game"]["generation"]}')

        if self.ai_training_mode:
            self.screen.blit(generation, (50, 380))

        self.screen.blit(points, (50, 300))
        self.screen.blit(time, (50, 340))

    def blit_buttons(self):
        self.screen.blit(self.menu_button.image, self.menu_button.rect)
        self.screen.blit(self.play_button.image, self.play_button.rect)

    def blit_screen(self):
        self.blit_background()
        self.blit_title()
        self.blit_content()
        self.blit_buttons()

    def check_button_pressed(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.menu_button.check_pressed(mouse_position, mouse_pressed):
            return "MENU"

        if self.play_button.check_pressed(mouse_position, mouse_pressed):
            return "GAME"

    def get_event_type(self, event):
        match event.type:
            case pygame.QUIT:
                return "QUIT"
            case _:
                return event.type
