import pygame
import Constants as C
import os
from main import resource_path

class ScreenManager:
    def __init__(self):
        self.current_state = "start"
        self.screen = pygame.display.set_mode((C.WIDTH, C.HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.buttons = [
            {"rect": pygame.Rect(700, 100, 60, 40), "color": C.WHITE, "hover_color": C.GREY, "snake_color": C.WHITE},
            {"rect": pygame.Rect(700, 170, 60, 40), "color": C.GREEN, "hover_color": (0, 200, 0), "snake_color": C.GREEN},
            {"rect": pygame.Rect(700, 240, 60, 40), "color": C.ORANGE, "hover_color": (255, 140, 0), "snake_color": C.ORANGE},
            {"rect": pygame.Rect(700, 310, 60, 40), "color": C.YELLOW, "hover_color": (200, 200, 0), "snake_color": C.YELLOW},
            {"rect": pygame.Rect(700, 380, 60, 40), "color": C.PINK, "hover_color": (255, 90, 130), "snake_color": C.PINK},
            {"rect": pygame.Rect(700, 450, 60, 40), "color": C.BLACK, "hover_color": (50, 50, 50), "snake_color": C.BLACK},
            {"rect": pygame.Rect(700, 520, 60, 40), "color": C.GREY, "hover_color": (100, 100, 100), "snake_color": C.GREY},
        ]

        self.game_over_buttons = [
            {"rect": pygame.Rect(C.WIDTH // 2 - 100, C.HEIGHT // 2 + 50, 200, 50), "text": "Restart", "action": "restart", "color": C.WHITE,"hover_color": C.GREY},
            {"rect": pygame.Rect(C.WIDTH // 2 - 100, C.HEIGHT // 2 + 120, 200, 50), "text": "Quit", "action": "quit", "color": C.WHITE, "hover_color": C.GREY},
        ]

        self.pause_buttons = [
            {"rect": pygame.Rect(C.WIDTH // 2 - 100, C.HEIGHT // 2 + 50, 200, 50), "text": "Resume", "action": "resume", "color": C.WHITE, "hover_color": C.GREY},
            {"rect": pygame.Rect(C.WIDTH // 2 - 100, C.HEIGHT // 2 + 120, 200, 50), "text": "Quit", "action": "quit", "color": C.WHITE, "hover_color": C.GREY},
        ]

    def transition_to(self, snake, score_manager=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.current_state == "start":
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            snake.color = button["snake_color"]
                elif self.current_state == "game_over":
                    for button in self.game_over_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["action"] == "restart":
                                snake.reset()
                                if score_manager:
                                    score_manager.reset_score()
                                self.current_state = "start"
                                return True
                            elif button["action"] == "quit":
                                pygame.quit()
                                exit()
                elif self.current_state == "pause":
                    for button in self.pause_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["action"] == "resume":
                                self.current_state = "game"
                            elif button["action"] == "quit":
                                pygame.quit()
                                exit()
                
            if event.type == pygame.KEYDOWN:
                if self.current_state == "start" and event.key == pygame.K_SPACE:
                    self.current_state = "game"
                elif self.current_state == "game" and event.key == pygame.K_SPACE:
                    self.current_state = "pause"

                if self.current_state == "game":
                    if event.key == pygame.K_UP:
                        snake.change_direction("UP")
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction("DOWN")
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction("RIGHT")
        return False

    def draw(self,snake,fruit, score_manager, obstacle=None):
        self.screen.fill(C.BLACK) 
        if self.current_state == "start":
            self.draw_start_screen()
        elif self.current_state == "game":
            self.draw_game_screen(snake,fruit,obstacle)
            score_manager.draw(self.screen)
        elif self.current_state == "pause":
            self.draw_pause_screen()
        elif self.current_state == "game_over":
            self.draw_game_over_screen(score_manager)
        pygame.display.flip()

    def draw_start_screen(self):
        bg = pygame.image.load(resource_path(os.path.join("images/background.jpg")))
        bg = pygame.transform.scale(bg, (C.WIDTH, C.HEIGHT))
        self.screen.blit(bg, (0, 0))
        font = pygame.font.Font(None, 40)
        start_text = font.render("Press Space to Start", True, C.WHITE)
        self.screen.blit(start_text, (C.WIDTH // 2 - start_text.get_width() // 2, C.HEIGHT // 2 - start_text.get_height() // 2)) 
        snake_color_text = font.render("Choose a color for your snake", True, C.WHITE)
        self.screen.blit(snake_color_text, (C.WIDTH // 2 - snake_color_text.get_width() // 2, C.HEIGHT // 2 - snake_color_text.get_height() // 2 - 50))

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            button_color = button["hover_color"] if is_hovered else button["color"]
            pygame.draw.rect(self.screen, button_color, button["rect"])
            pygame.draw.rect(self.screen, button["snake_color"], button["rect"], 3)

    def draw_game_screen(self,snake,fruit, obstacles=None):
        pygame.draw.rect(self.screen, C.BLUE, (C.GRID_OFFSET_X, C.GRID_OFFSET_Y, C.GRID_WIDTH, C.GRID_HEIGHT))
        snake.draw(self.screen)
        fruit.draw(self.screen)

        if obstacles:
            if obstacles and len(obstacles.obstacles) > 0:
                obstacles.draw(self.screen)

        font = pygame.font.Font(None, 40)
        text = font.render("Eat as many fruits as you can!", True, C.WHITE)
        self.screen.blit(text, (C.GRID_OFFSET_X, C.GRID_OFFSET_Y + C.GRID_HEIGHT + 20))

        pause_text = font.render("Press SPACE to pause", True, C.WHITE)
        self.screen.blit(pause_text, (C.GRID_OFFSET_X, C.GRID_OFFSET_Y + C.GRID_HEIGHT + 60))
        
    def draw_pause_screen(self):
        font = pygame.font.Font(None, 40)
        text = font.render("Paused", True, C.WHITE)
        self.screen.blit(text, (C.WIDTH // 2 - text.get_width() // 2, C.HEIGHT // 2 - text.get_height() // 2)) 

        mouse_pos = pygame.mouse.get_pos()
        for button in self.pause_buttons:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            button_color = button["hover_color"] if is_hovered else button["color"]

            pygame.draw.rect(self.screen, button_color, button["rect"])
            font = pygame.font.Font(None, 30)
            text = font.render(button["text"], True, C.BLACK)
            self.screen.blit(text, (button["rect"].x + 65, button["rect"].y + 15))

    def draw_game_over_screen(self, score_manager):
        font = pygame.font.Font(None, 40)
        game_over_text = font.render("Game Over", True, C.WHITE)
        self.screen.blit(game_over_text, (C.WIDTH // 2 - game_over_text.get_width() // 2, C.HEIGHT // 2 - game_over_text.get_height() // 2 - 100)) 

        score_text = font.render(f"Final Score: {score_manager.score}", True, C.WHITE)
        self.screen.blit(score_text, (C.WIDTH // 2 - score_text.get_width() // 2, C.HEIGHT // 2 - 80))

        high_score_text = font.render(f"High Score: {score_manager.high_score}", True, C.WHITE)
        self.screen.blit(high_score_text, (C.WIDTH // 2 - high_score_text.get_width() // 2, C.HEIGHT // 2 - 50))

        mouse_pos = pygame.mouse.get_pos()
        for button in self.game_over_buttons:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            button_color = button["hover_color"] if is_hovered else button["color"]

            pygame.draw.rect(self.screen, button_color, button["rect"])
            font = pygame.font.Font(None, 30)
            text = font.render(button["text"], True, C.BLACK)
            self.screen.blit(text, (button["rect"].x + 65, button["rect"].y + 15))