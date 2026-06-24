import pygame
from pygame.locals import (RLEACCEL)
from resources import load_image, screen_width, screen_height
import random

class CrMeteor(pygame.sprite.Sprite):
    def __init__(self):
        super(CrMeteor, self).__init__()
        src_w, src_h = 501, 227

        random_scale = random.uniform(1.5, 2.8)
        comet_w = int(src_w / random_scale)
        comet_h = int(src_h / random_scale)

        comet_img = load_image("comet.png", (comet_w, comet_h))
        self.surf = pygame.transform.rotate(comet_img, 220)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # Meteors only spawn in the top half so it feels like they're falling
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 30, screen_width + 90),
                random.randint(0, screen_height // 2)
            )
        )
        self.speed = random.randint(1, 4)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

