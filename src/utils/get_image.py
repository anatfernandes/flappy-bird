import os
import pygame


def get_image(image):
    image_name = f"{image}.png"
    pygame_image = pygame.image.load(os.path.join("images", image_name))

    return pygame.transform.scale2x(pygame_image)
