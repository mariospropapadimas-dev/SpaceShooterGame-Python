import os
import pygame
from pygame.locals import (RLEACCEL,K_ESCAPE, KEYDOWN, QUIT)
from player import CrPlayer
from enemy import CrEnemy
from meteor import CrMeteor
from shield import CrShield
from heal import CrHeal
from gamestate import GameState
from resources import load_image, screen_width, screen_height

# TODO: Add high score tracking using the time library

pygame.init()


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# load and scale images without crashing the game if a file is missing


# Stretch background to fit the screen
bg = load_image("bg.png", (screen_width, screen_height))


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
pygame.time.set_timer(AddShieldPowerUp, 27000)
pygame.time.set_timer(AddHealPowerUp, 12000)

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

    # 2. Update game
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

    # powerups
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
