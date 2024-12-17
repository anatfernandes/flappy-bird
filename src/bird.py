import os
import pygame


BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png"))),
]


class Bird:
    IMAGES = BIRD_IMAGES
    # animações da rotação
    MAXIMUM_ROTATION = 25
    ROTATION_SPEED = 20
    TIME_ANIMATION = 5

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
        # calcula o deslocamento
        self.time += 1
        shift = 1.5 * (self.time**2) + self.speed * self.time

        # restringe o deslocamento
        if shift > 16:
            shift = 16
        elif shift < 0:
            shift -= 2

        self.y += shift

        # ângulo do pássaro
        if shift < 0 or self.y < (self.height + 50):
            if self.angle < self.MAXIMUM_ROTATION:
                self.angle = self.MAXIMUM_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED

    def draw(self, screen):
        # define qual imagem do pássaro vai usar
        self.image_count += 1

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

        # se o pássaro tiver caindo não bate asas
        if self.angle <= -80:
            self.image = self.IMAGES[1]
            self.image_count = self.TIME_ANIMATION * 2

        # desenha a imagem
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        position_center_imagem = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=position_center_imagem)
        screen.blit(rotated_image, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
