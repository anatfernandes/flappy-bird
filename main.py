"""Flappy Bird Game"""

import os
import random
import pygame

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

PIPE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "pipe.png"))
)
FLOOR_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "floor.png"))
)
BACKGROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "background.png"))
)
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png"))),
]

pygame.font.init()
POINTS_FONT = pygame.font.SysFont("arial", 50)


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


class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_position = 0
        self.base_position = 0
        self.has_passed = False
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BASE = PIPE_IMAGE
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


class Floor:
    SPEED = 5
    WIDTH = FLOOR_IMAGE.get_width()
    IMAGE = FLOOR_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))


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
