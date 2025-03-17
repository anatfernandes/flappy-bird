import os
import pygame
import neat
import neat.config
import pickle

from .utils import get_image

from .bird import Bird
from .pipe import Pipe
from .floor import Floor


pygame.font.init()


class Game:
    BACKGROUND_IMAGE = get_image("background")

    POINTS_FONT = pygame.font.SysFont("arial", 32)

    def __init__(
        self, config, screen, clock, ai_genomes=None, ai_config=None, generation=0
    ):
        pygame.display.set_caption("Flappy Bird")

        self.initial_time = pygame.time.get_ticks()

        self.points = 0
        self.running = False
        self.ai_mode = False
        self.ai_training_mode = False
        self.clock = clock
        self.config = config
        self.screen = screen
        self.generation = generation
        self.SCREEN_WIDTH = config["SCREEN_WIDTH"]
        self.SCREEN_HEIGHT = config["SCREEN_HEIGHT"]

        self.set_speed()

        self.floor = Floor(y=730, speed=self.SPEED)
        self.pipes = [self.create_pipe()]
        self.birds = []

        self.ai_genomes = ai_genomes
        self.ai_config = ai_config
        self.networks = []
        self.bird_genomes = []

        self.set_game_mode()
        self.populate_ia_mode_fields()
        self.populate_birds()

    def run(self):
        root_path = os.path.abspath(os.curdir)
        path = os.path.join(root_path, "config.txt")
        self.init(path)

    def init(self, path):
        if not self.ai_training_mode:
            self.play()
            return

        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            path,
        )

        population = neat.Population(config)

        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.StatisticsReporter())

        population.run(self.start, 50)

        self.update_config()

    def start(self, ai_genomes=None, ai_config=None):
        self.__init__(
            self.config,
            self.screen,
            self.clock,
            ai_genomes,
            ai_config,
            generation=self.generation + 1,
        )

        self.play()

    def play(self):
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

            if self.end_game():
                self.update_config()
                break

            self.draw_screen(
                self.screen, self.birds, self.pipes, self.floor, self.points
            )

    def create_bird(self):
        return Bird(x=230, y=350)

    def create_pipe(self, x=700):
        return Pipe(x, speed=self.SPEED, config=self.config)

    def end_game(self):
        return not len(self.birds)

    def set_speed(self):
        self.SPEED = {"Fácil": 3, "Normal": 5, "Difícil": 7, "Impossível": 10}[
            self.config["difficulties"]["current"]
        ]

    def set_game_mode(self):
        mode = self.config["modes"][self.config["modes"]["current"]]

        self.ai_mode = mode == "IA"
        self.ai_training_mode = mode == "IA_TRAIN"

    def populate_ia_mode_fields(self):
        if not self.ai_mode:
            return

        with open("ai_mode.pkl", "rb") as file:
            ai = pickle.load(file)
            self.networks = [ai["network"]]
            self.bird_genomes = [ai["genome"]]

    def populate_birds(self):
        if self.ai_training_mode and not self.ai_genomes:
            return

        if not self.ai_training_mode:
            self.birds.append(self.create_bird())
            return

        for _, genome in self.ai_genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, self.ai_config)
            genome.fitness = 0

            self.networks.append(network)
            self.bird_genomes.append(genome)
            self.birds.append(self.create_bird())

    def add_pipe(self):
        self.points += 1
        self.pipes.append(self.create_pipe(x=600))

        self.update_bird_fitness(5)

    def remove_pipe(self, pipe):
        self.pipes.remove(pipe)

    def remove_bird(self, index):
        self.birds.pop(index)

        if self.ai_training_mode:
            self.update_bird_fitness(-1, index)
            self.bird_genomes.pop(index)
            self.networks.pop(index)

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
                self.remove_bird(i)

    def move_entities(self):
        for i, bird in enumerate(self.birds):
            bird.move()
            self.jump_ai_bird(bird, i)

        self.floor.move()

        self.track_pipes()

    def jump_ai_bird(self, bird, index):
        if not self.ai_training_mode and not self.ai_mode:
            return

        self.update_bird_fitness(0.1, index)

        next_pipe_index = self.get_next_pipe_index()
        next_pipe = self.pipes[next_pipe_index]

        output = self.networks[index].activate(
            (
                bird.y,
                abs(bird.y - next_pipe.top_position),
                abs(bird.y - next_pipe.base_position),
            )
        )

        if output[0] > 0.5:
            bird.jump()

    def update_bird_fitness(self, value, index=None):
        if not self.ai_training_mode:
            return

        if index:
            self.bird_genomes[index].fitness += value
            return

        for genome in self.bird_genomes:
            genome.fitness += value

    def update_config(self):
        self.config["game"]["points"] = self.points
        self.config["game"]["generation"] = self.generation
        self.config["game"]["time"] = self.get_game_time()
        self.config["page"] = "END_GAME"

    def get_game_time(self):
        return (pygame.time.get_ticks() - self.initial_time) // 1000

    def get_event_type(self, event):
        match event.type:
            case pygame.QUIT:
                return "QUIT"
            case pygame.KEYDOWN:
                space_pressed = event.key == pygame.K_SPACE
                player_mode = not self.ai_training_mode and not self.ai_mode

                return "JUMP" if space_pressed and player_mode else event.key
            case _:
                return event.type

    def get_next_pipe_index(self):
        has_pipes = len(self.pipes) > 1
        first_pipe_position = self.pipes[0].x + self.pipes[0].PIPE_TOP.get_width()
        bird_has_passed = self.birds[0].x > first_pipe_position

        if has_pipes and bird_has_passed:
            return 1

        return 0

    def blit_texts(self, screen, points):
        color = (255, 255, 255)
        antialias = 1

        points_message = f"Pontuação: {points}"
        time_message = f"Tempo: {self.get_game_time()}s"
        generation_message = f"Geração: {self.generation}"

        points_text = self.POINTS_FONT.render(points_message, antialias, color)
        points_text_x_position = self.SCREEN_WIDTH - 10 - points_text.get_width()

        time_text = self.POINTS_FONT.render(time_message, antialias, color)
        time_text_x_position = self.SCREEN_WIDTH - 10 - time_text.get_width()

        generation_text = self.POINTS_FONT.render(generation_message, antialias, color)

        if self.ai_training_mode:
            screen.blit(generation_text, (10, 10))

        screen.blit(points_text, (points_text_x_position, 10))
        screen.blit(time_text, (time_text_x_position, 50))

    def draw_screen(self, screen, birds, pipes, floor, points):
        screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        for bird in birds:
            bird.draw(screen)

        for pipe in pipes:
            pipe.draw(screen)

        floor.draw(screen)

        self.blit_texts(screen, points)

        pygame.display.update()
