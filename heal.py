import pygame
from pygame.locals import (RLEACCEL)
from resources import load_image, screen_width, screen_height
import random

class CrHeal(pygame.sprite.Sprite):
    def __init__(self):
        super(CrHeal, self).__init__()
        src_w, src_h = 285, 347

        w = int(src_w // 3)
        h = int(src_h // 3)

        self.surf = load_image("heal.png", (w, h))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 30, screen_width + 90),
                random.randint(0, screen_height)
            )
        )
        self.speed = random.randint(1, 4)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()