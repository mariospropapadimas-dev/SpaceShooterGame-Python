import os
import pygame
from pygame.locals import (RLEACCEL, K_w, K_s, K_a, K_d, K_ESCAPE, KEYDOWN, QUIT)
import random

# TODO: Add high score tracking using the time library

pygame.init()

# Window dimensions. Change these and the game logic should scale mostly fine.
screen_width = 1307
screen_height = 816

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Helper to load and scale images without crashing the game if a file is missing
BASE_DIR = os.path.dirname(__file__)


def load_image(name, scale=None):
    path = os.path.join(BASE_DIR, name)
    try:
        img = pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"Error loading image '{path}': {e}")
        raise SystemExit(e)

    if scale:
        img = pygame.transform.scale(img, scale)
    return img


# Stretch background to fit the screen
bg = load_image("bg.png", (screen_width, screen_height))


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
        self.rect.clamp_ip(screen.get_rect())


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


class GameState:
    """Tracks global game variables like timers."""

    def __init__(self):
        self.shield_active = False
        self.shield_end_time = 0

    def activate_shield(self, duration_ms):
        self.shield_active = True
        self.shield_end_time = pygame.time.get_ticks() + duration_ms


# --- Setup Groups & Timers ---
Player = CrPlayer()
all_Sprites = pygame.sprite.Group()
all_Sprites.add(Player)

pawns = pygame.sprite.Group()
enemies = pygame.sprite.Group()
shields = pygame.sprite.Group()
heals = pygame.sprite.Group()

font = pygame.font.Font(None, 36)
state = GameState()

# Custom events for spawning
AddSpaceshipEnemy = pygame.USEREVENT + 1
AddMeteorEnemy = pygame.USEREVENT + 2
AddShieldPowerUp = pygame.USEREVENT + 3
AddHealPowerUp = pygame.USEREVENT + 4

pygame.time.set_timer(AddSpaceshipEnemy, 2000)
pygame.time.set_timer(AddMeteorEnemy, 2300)
pygame.time.set_timer(AddShieldPowerUp, 15000)
pygame.time.set_timer(AddHealPowerUp, 7000)

clock = pygame.time.Clock()
running = True

# --- Main Game Loop ---
while running:
    # 1. Handle Events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

        # Spawners
        elif event.type == AddSpaceshipEnemy:
            new_enemy = CrEnemy()
            pawns.add(new_enemy)
            all_Sprites.add(new_enemy)
            enemies.add(new_enemy)

        elif event.type == AddMeteorEnemy:
            new_meteor = CrMeteor()
            pawns.add(new_meteor)
            all_Sprites.add(new_meteor)
            enemies.add(new_meteor)

        elif event.type == AddShieldPowerUp:
            new_shield = CrShield()
            pawns.add(new_shield)
            all_Sprites.add(new_shield)
            shields.add(new_shield)

        elif event.type == AddHealPowerUp:
            new_heal = CrHeal()
            all_Sprites.add(new_heal)
            pawns.add(new_heal)
            heals.add(new_heal)

    # 2. Update Physics
    pressed_keys = pygame.key.get_pressed()
    Player.update(pressed_keys)
    pawns.update()

    # 3. Draw Frame
    screen.blit(bg, (0, 0))
    for entity in all_Sprites:
        screen.blit(entity.surf, entity.rect)

    # 4. Handle Logic & Collisions
    # Check shield expiration
    if state.shield_active:
        Player.surf = Player.Spaceship_Shield_Image
        if pygame.time.get_ticks() > state.shield_end_time:
            state.shield_active = False
            Player.surf = Player.Spaceship_Image

    # Enemy hits (True = enemy is deleted on impact)
    collided_with_enemy = pygame.sprite.spritecollide(Player, enemies, True)
    if collided_with_enemy and not state.shield_active:
        Player.player_lives -= len(collided_with_enemy)
        if Player.player_lives <= 0:
            running = False

    # Powerups
    collided_with_shield = pygame.sprite.spritecollide(Player, shields, not state.shield_active)
    if collided_with_shield and not state.shield_active:
        state.activate_shield(10000)  # 10s of god mode

    collided_with_heal = pygame.sprite.spritecollide(Player, heals, True)
    if collided_with_heal and Player.player_lives < 10:
        Player.player_lives = min(10, Player.player_lives + len(collided_with_heal))

    # HUD
    lives_surf = font.render(f"Lives: {Player.player_lives}", True, (255, 255, 255))
    screen.blit(lives_surf, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
