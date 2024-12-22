import pygame

from .utils import get_image

from .bird import Bird
from .pipe import Pipe
from .floor import Floor


pygame.font.init()


class Game:
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 800

    BACKGROUND_IMAGE = get_image("background")

    POINTS_FONT = pygame.font.SysFont("arial", 50)

    def __init__(self):
        self.points = 0
        self.clock = pygame.time.Clock()

        self.floor = Floor(730)
        self.pipes = [Pipe(700)]
        self.birds = [Bird(230, 350)]

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def start(self):
        running = True

        while running:
            self.clock.tick(30)

            # interação com o usuário
            for event in pygame.event.get():
                print(event.type)
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    for bird in self.birds:
                        bird.jump()

            # mover as coisas
            for bird in self.birds:
                bird.move()

            self.floor.move()

            add_pipe = False
            remove_pipes = []

            for pipe in self.pipes:
                for i, bird in enumerate(self.birds):
                    if pipe.collide(bird):
                        self.birds.pop(i)

                    if not pipe.has_passed and bird.x > pipe.x:
                        pipe.has_passed = True
                        add_pipe = True

                pipe.move()

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    remove_pipes.append(pipe)

            if add_pipe:
                self.points += 1
                self.pipes.append(Pipe(600))

            for pipe in remove_pipes:
                self.pipes.remove(pipe)

            for i, bird in enumerate(self.birds):
                if (bird.y + bird.image.get_height()) > self.floor.y or bird.y < 0:
                    self.birds.pop(i)

            self.draw_screen(
                self.screen, self.birds, self.pipes, self.floor, self.points
            )

    def draw_screen(self, screen, birds, pipes, floor, points):
        screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        for bird in birds:
            bird.draw(screen)

        for pipe in pipes:
            pipe.draw(screen)

        points_text = self.POINTS_FONT.render(
            f"Pontuação: {points}", 1, (255, 255, 255)
        )
        screen.blit(points_text, (self.SCREEN_WIDTH - 10 - points_text.get_width(), 10))

        floor.draw(screen)
        pygame.display.update()
