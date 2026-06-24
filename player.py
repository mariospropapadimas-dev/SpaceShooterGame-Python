import pygame
from pygame.locals import (RLEACCEL, K_w, K_s, K_a, K_d)
from resources import load_image, screen_width, screen_height


class CrPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super(CrPlayer, self).__init__()
        self.player_lives = 10
        self.speed = 4

        self.SpaceshipImageWidth = 382
        self.SpaceshipImageHeight = 239
        self.Spaceship_Shield_Image_Width = 446
        self.Spaceship_Shield_Image_Height = 274

        # Preload both ship states so we can hot-swap them later
        self.Spaceship_Shield_Image = load_image(
            "Spaceship_Shield.png",
            (self.Spaceship_Shield_Image_Width // 2.5,
             self.Spaceship_Shield_Image_Height // 2.5)
        )
        self.Spaceship_Image = load_image(
            "Spaceship.png",
            (self.SpaceshipImageWidth // 2,
             self.SpaceshipImageHeight // 2)
        )

        self.surf = self.Spaceship_Image
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        # Start mid-left
        self.rect.center = (screen_width // 6, screen_height // 2)

    def update(self, keys_pressed):
        # WASD Movement
        if keys_pressed[K_w]: self.rect.move_ip(0, -self.speed)
        if keys_pressed[K_s]: self.rect.move_ip(0, self.speed)
        if keys_pressed[K_a]: self.rect.move_ip(-self.speed, 0)
        if keys_pressed[K_d]: self.rect.move_ip(self.speed, 0)

        # Keep the player inside the screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))
