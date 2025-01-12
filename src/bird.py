import pygame

from .utils import get_image


class Bird:
    IMAGES = [
        get_image("bird1"),
        get_image("bird2"),
        get_image("bird3"),
    ]

    # animações da rotação
    MAXIMUM_ROTATION = 25
    ROTATION_SPEED = 20
    TIME_ANIMATION = 5
    ACELERATION = 3

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.time = 0
        self.angle = 0
        self.speed = 0
        self.image_count = 0

        self.height = self.y
        self.image = self.IMAGES[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        self.time += 1

        # ((1/2) * ​a * t²) + (v0​ * t)
        shift = 0.5 * self.ACELERATION * (self.time**2) + self.speed * self.time

        if shift > 16:
            shift = 16
        elif shift < 0:
            shift -= 2

        self.y += shift

        self.set_angle(shift)

    def draw(self, screen):
        self.set_image()

        rotated_image = pygame.transform.rotate(self.image, self.angle)
        position_center_imagem = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=position_center_imagem)

        screen.blit(rotated_image, rectangle.topleft)

    def set_angle(self, shift):
        is_negative_shift = shift < 0
        is_valid_position = self.y < (self.height + 50)
        is_valid_angle = self.angle < self.MAXIMUM_ROTATION

        if (is_negative_shift or is_valid_position) and is_valid_angle:
            self.angle = self.MAXIMUM_ROTATION

        elif self.angle > -90:
            self.angle -= self.ROTATION_SPEED

    def set_image(self):
        self.image_count += 1

        if self.angle <= -80:
            self.image = self.IMAGES[1]
            self.image_count = self.TIME_ANIMATION * 2
            return

        if self.image_count < self.TIME_ANIMATION:
            self.image = self.IMAGES[0]
        elif self.image_count < self.TIME_ANIMATION * 2:
            self.image = self.IMAGES[1]
        elif self.image_count < self.TIME_ANIMATION * 3:
            self.image = self.IMAGES[2]
        elif self.image_count < self.TIME_ANIMATION * 4:
            self.image = self.IMAGES[1]
        elif self.image_count < self.TIME_ANIMATION * 4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
