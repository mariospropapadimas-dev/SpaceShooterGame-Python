import pygame
from pygame.locals import (RLEACCEL)
from resources import load_image, screen_width, screen_height
from player import CrPlayer as Player
import random

class CrShield(pygame.sprite.Sprite):
    def __init__(self):
        super(CrShield, self).__init__()
        shield_img = load_image("shield.png")
        orig_w, orig_h = shield_img.get_size()

        # Scale relative to player size if possible
        try:
            desired_w = int(Player.surf.get_width() * 0.5)
        except Exception:
            desired_w = int(screen_width / 6)

        scale = desired_w / orig_w if orig_w else 1.0
        shield_w = max(1, int(orig_w * scale))
        shield_h = max(1, int(orig_h * scale))

        self.surf = pygame.transform.scale(shield_img, (shield_w, shield_h))
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

