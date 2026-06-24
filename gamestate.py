import pygame
import time

class GameState:
    #Tracks global game variables like timers.

    def __init__(self):
        self.shield_active = False
        self.shield_end_time = 0
        self.game_start_time = time.time()
        self.high_score = self.load_high_score()

    def activate_shield(self, duration_ms):
        self.shield_active = True
        self.shield_end_time = pygame.time.get_ticks() + duration_ms

    def get_current_score(self):
        #Returns current survival time in seconds
        return int(time.time() - self.game_start_time)

    def load_high_score(self):
        #Load high score from file, return 0 if file is empty or doesn't exist
        try:
            with open("highscore.txt", "r") as f:
                content = f.read().strip()
                return int(content) if content else 0
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self, score):
        #Save high score to file
        with open("highscore.txt", "w") as f:
            f.write(str(score))