import random
import pygame

from .utils import get_image


class Pipe:
    IMAGE = get_image("pipe")

    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_position = 0
        self.base_position = 0
        self.has_passed = False
        self.PIPE_TOP = pygame.transform.flip(self.IMAGE, False, True)
        self.PIPE_BASE = self.IMAGE
        self.set_height()

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
