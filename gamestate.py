import pygame

class GameState:
    #Tracks global game variables like timers.

    def __init__(self):
        self.shield_active = False
        self.shield_end_time = 0

    def activate_shield(self, duration_ms):
        self.shield_active = True
        self.shield_end_time = pygame.time.get_ticks() + duration_ms