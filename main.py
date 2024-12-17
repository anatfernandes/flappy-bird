"""Flappy Bird Game"""

import os
import pygame

from src.bird import Bird
from src.pipe import Pipe
from src.floor import Floor


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

BACKGROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "background.png"))
)

pygame.font.init()
POINTS_FONT = pygame.font.SysFont("arial", 50)


def draw_screen(screen, birds, pipes, floor, points):
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    for bird in birds:
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)

    points_text = POINTS_FONT.render(f"Pontuação: {points}", 1, (255, 255, 255))
    screen.blit(points_text, (SCREEN_WIDTH - 10 - points_text.get_width(), 10))

    floor.draw(screen)
    pygame.display.update()


def main():
    points = 0
    clock = pygame.time.Clock()

    floor = Floor(730)
    pipes = [Pipe(700)]
    birds = [Bird(230, 350)]

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True

    while running:
        clock.tick(30)

        # interação com o usuário
        for event in pygame.event.get():
            print(event.type)
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for bird in birds:
                    bird.jump()

        # mover as coisas
        for bird in birds:
            bird.move()

        floor.move()

        add_pipe = False
        remove_pipes = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)

                if not pipe.has_passed and bird.x > pipe.x:
                    pipe.has_passed = True
                    add_pipe = True

            pipe.move()

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipes.append(pipe)

        if add_pipe:
            points += 1
            pipes.append(Pipe(600))

        for pipe in remove_pipes:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)

        draw_screen(screen, birds, pipes, floor, points)


if __name__ == "__main__":
    main()
