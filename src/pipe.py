import random
import pygame

from .utils import get_image


class Pipe:
    PIPE_BASE = get_image("pipe")
    PIPE_TOP = pygame.transform.flip(PIPE_BASE, False, True)

    DISTANCE = 200
    SPEED = 5

    def __init__(self, x, config, speed=5):
        self.x = x
        self.config = config
        self.SPEED = speed

        self.height = 0
        self.top_position = 0
        self.base_position = 0

        self.has_passed = False
        self.passing = False

        self.set_distance()
        self.set_height()

    def set_distance(self):
        current_difficulty = self.config["difficulties"]["current"]
        distance_by_difficult = {
            "EASY": 300,
            "NORMAL": 220,
            "HARD": 200,
            "IMPOSSIBLE": 200,
        }[self.config["difficulties"][current_difficulty]]

        self.DISTANCE = distance_by_difficult

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top_position = self.height - self.PIPE_TOP.get_height()
        self.base_position = self.height + self.DISTANCE

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.top_position))
        screen.blit(self.PIPE_BASE, (self.x, self.base_position))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        base_mask = pygame.mask.from_surface(self.PIPE_BASE)

        top_distance = (self.x - bird.x, self.top_position - round(bird.y))
        base_distance = (self.x - bird.x, self.base_position - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_distance)
        base_point = bird_mask.overlap(base_mask, base_distance)

        return base_point or top_point

    def update_has_passed(self, bird):
        if bird.x > self.x:
            if not self.has_passed and self.passing:
                self.has_passed = True
                self.passing = False

            if not self.has_passed:
                self.passing = True
