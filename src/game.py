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
        while True:
            self.clock.tick(30)

            # interação com o usuário
            for event in pygame.event.get():
                event_type = self.get_event_type(event)

                if event_type == "QUIT":
                    pygame.quit()
                    quit()
                    break

                if event_type == "JUMP":
                    for bird in self.birds:
                        bird.jump()

            # mover as coisas
            for bird in self.birds:
                bird.move()

            self.floor.move()

            for pipe in self.pipes:
                tracked_birds = self.track_birds(pipe)

                if tracked_birds["add_pipe"]:
                    pipe.has_passed = True
                    self.add_pipe()

                pipe.move()

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    self.remove_pipe(pipe)

            self.draw_screen(
                self.screen, self.birds, self.pipes, self.floor, self.points
            )

    def add_pipe(self):
        self.points += 1
        self.pipes.append(Pipe(600))

    def remove_pipe(self, pipe):
        self.pipes.remove(pipe)

    def track_birds(self, pipe):
        add_pipe = False

        for i, bird in enumerate(self.birds):
            bird_height = bird.y + bird.image.get_height()

            has_bird_collide_with_floor = bird_height > self.floor.y
            has_bird_collide_with_roof = bird.y < 0

            remove_bird = (
                pipe.collide(bird)
                or has_bird_collide_with_floor
                or has_bird_collide_with_roof
            )

            if remove_bird:
                self.birds.pop(i)

            if not pipe.has_passed and bird.x > pipe.x:
                add_pipe = True

        return {"add_pipe": add_pipe}

    def get_event_type(self, event):
        match event.type:
            case pygame.QUIT:
                return "QUIT"
            case pygame.KEYDOWN:
                return "JUMP" if event.key == pygame.K_SPACE else event.key
            case _:
                return event.type

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
