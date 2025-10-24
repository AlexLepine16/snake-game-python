import pygame
import Constants as C

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()
        

    def increment_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        

    def reset_score(self):
        self.score = 0

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

    def draw(self,screen):
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {self.score}", True, C.WHITE)
        high_score_text = font.render(f"High Score: {self.high_score}", True, C.WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

    def draw_game_over(self, screen):
        font = pygame.font.SysFont("Arial", 50)
        score_text = font.render(f"Final Score: {self.score}", True, C.WHITE)
        high_score_text = font.render(f"High Score: {self.high_score}", True, C.WHITE)
        screen.blit(score_text, (C.WIDTH // 2 - score_text.get_width() // 2, C.HEIGHT // 2 - 50))
        screen.blit(high_score_text, (C.WIDTH // 2 - high_score_text.get_width() // 2, C.HEIGHT // 2))