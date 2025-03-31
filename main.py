"""Flappy Bird Game"""

import pygame

from src.game import Game
from src.menu import Menu
from src.end_game import EndGame
from src.settings import Settings


def main():
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 800

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    config = {
        "page": "MENU",
        "game": {"points": 0, "time": 0, "generation": 0},
        "modes": {
            "Usuário": "USER",
            "IA": "IA",
            "Treino IA": "IA_TRAIN",
            "current": "USER",
        },
        "difficulties": {
            "Fácil": "EASY",
            "Normal": "NORMAL",
            "Difícil": "HARD",
            "Impossível": "IMPOSSIBLE",
            "current": "Normal",
        },
        "SCREEN_WIDTH": SCREEN_WIDTH,
        "SCREEN_HEIGHT": SCREEN_HEIGHT,
    }

    while True:
        match config["page"]:
            case "MENU":
                menu = Menu(config, screen, clock)
                menu.run()
            case "GAME":
                game = Game(config, screen, clock)
                game.run()
            case "SETTINGS":
                settings = Settings(config, screen, clock)
                settings.run()
            case "END_GAME":
                end_game = EndGame(config, screen, clock)
                end_game.run()


if __name__ == "__main__":
    main()
