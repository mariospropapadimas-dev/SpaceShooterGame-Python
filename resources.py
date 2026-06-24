import os
import pygame

screen_width = 1307
screen_height = 816
BASE_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_image(name, scale=None):
    path = os.path.join(BASE_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img
