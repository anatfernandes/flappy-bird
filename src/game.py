import pygame

from .utils import get_image

from .bird import Bird
from .pipe import Pipe
from .floor import Floor


pygame.font.init()


class Game:
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 800
    SPEED = 5

    BACKGROUND_IMAGE = get_image("background")

    POINTS_FONT = pygame.font.SysFont("arial", 32)

    def __init__(self):
        pygame.display.set_caption("Flappy Bird")

        self.points = 0
        self.clock = pygame.time.Clock()

        self.floor = Floor(y=730, speed=self.SPEED)
        self.pipes = [Pipe(x=700, speed=self.SPEED)]
        self.birds = [Bird(x=230, y=350)]

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def start(self):
        while True:
            self.clock.tick(30)

            for event in pygame.event.get():
                event_type = self.get_event_type(event)

                if event_type == "QUIT":
                    pygame.quit()
                    quit()
                    break

                if event_type == "JUMP":
                    for bird in self.birds:
                        bird.jump()

            self.move_entities()

            self.draw_screen(
                self.screen, self.birds, self.pipes, self.floor, self.points
            )

    def add_pipe(self):
        self.points += 1
        self.pipes.append(Pipe(x=600, speed=self.SPEED))

    def remove_pipe(self, pipe):
        self.pipes.remove(pipe)

    def track_pipes(self):
        for pipe in self.pipes:
            self.track_birds(pipe)

            if len(self.birds) > 0:
                pipe.update_has_passed(self.birds[0])

                if pipe.passing:
                    self.add_pipe()

            pipe.move()

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                self.remove_pipe(pipe)

    def track_birds(self, pipe):
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

    def move_entities(self):
        for bird in self.birds:
            bird.move()

        self.floor.move()

        self.track_pipes()

    def get_event_type(self, event):
        match event.type:
            case pygame.QUIT:
                return "QUIT"
            case pygame.KEYDOWN:
                return "JUMP" if event.key == pygame.K_SPACE else event.key
            case _:
                return event.type

    def blit_texts(self, screen, points):
        points_message = f"Pontuação: {points}"
        color = (255, 255, 255)
        antialias = 1

        points_text = self.POINTS_FONT.render(points_message, antialias, color)
        points_text_x_position = self.SCREEN_WIDTH - 10 - points_text.get_width()

        screen.blit(points_text, (points_text_x_position, 10))

    def draw_screen(self, screen, birds, pipes, floor, points):
        screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        for bird in birds:
            bird.draw(screen)

        for pipe in pipes:
            pipe.draw(screen)

        floor.draw(screen)

        self.blit_texts(screen, points)

        pygame.display.update()
