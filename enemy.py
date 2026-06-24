import pygame
from pygame.locals import (RLEACCEL)
from resources import load_image, screen_width, screen_height
import random

class CrEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super(CrEnemy, self).__init__()
        src_w, src_h = 555, 258

        # Randomize enemy size to mix things up
        random_scale = random.uniform(1.5, 2.8)
        enemy_w = int(src_w / random_scale)
        enemy_h = int(src_h / random_scale)

        self.surf = load_image("enemy1.png", (enemy_w, enemy_h))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # Spawn off-screen to the right
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

