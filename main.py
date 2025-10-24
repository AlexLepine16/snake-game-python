import pygame
import ScreenManager as SM
import ScoreManager as ScM
import Snake
import Fruit
import Obstacle
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource for dev and for PyInstaller bundle."""
    try:
        base_path = sys._MEIPASS  
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    pygame.init()
    pygame.mixer.init()
    background_music = pygame.mixer.Sound(resource_path(os.path.join('sounds', 'music.wav')))
    eat_sound = pygame.mixer.Sound(resource_path(os.path.join('sounds', 'eat_sound.wav')))
    death_sound = pygame.mixer.Sound(resource_path(os.path.join('sounds', 'death_sound.wav')))
    death_sound.set_volume(1.0)
    background_music.set_volume(0.8)
    background_music.play(-1)
    screen_manager = SM.ScreenManager()
    score_manager = ScM.ScoreManager()
    snake = Snake.Snake()
    obstacle = Obstacle.Obstacle(snake) 
    fruit = Fruit.Fruit(snake, obstacle.obstacles)
    clock = pygame.time.Clock()
    
    # Game state variables
    clock_speed = 8
    last_incremented_score = 0
    obstacle_interval = 10
    game_over = False
    final_score = 0  # Stores the score when game ended

    while True:
        # Handle input/transitions (returns True if game was restarted)
        if screen_manager.transition_to(snake, score_manager):
            # Reset game state for new game
            game_over = False
            clock_speed = 8
            last_incremented_score = 0
            fruit = Fruit.Fruit(snake, obstacle.obstacles)
            obstacle.obstacles = []

        # Draw the appropriate screen
        if game_over:
            # Show game over screen with preserved final score
            screen_manager.draw(snake, fruit, score_manager, obstacle)
        else:
            # Normal game screen
            screen_manager.draw(snake, fruit, score_manager, obstacle)

        # Game logic (only when playing)
        if screen_manager.current_state == "game" and not game_over:
            # Movement and scoring
            snake.move()
            if snake.body[0][0] == fruit.position[0] and snake.body[0][1] == fruit.position[1]:
                score_manager.increment_score()
                snake.move(grow=True)
                fruit = Fruit.Fruit(snake, obstacle.obstacles)
                eat_sound.play()

                # Obstacle spawning every 10 fruits and then 1 more after every 10
                if (score_manager.score > 0 and 
                    score_manager.score % obstacle_interval == 0 and 
                    score_manager.score != last_incremented_score):

                    if score_manager.score == obstacle_interval:
                        obstacle.spawn()

                    else:
                        obstacle.spawn(additional=True)

            # Collision detection
            if snake.body[0] in obstacle.obstacles or snake.check_collision():
                game_over = True
                final_score = score_manager.score
                screen_manager.current_state = "game_over"
                death_sound.play()

            # Speed increase
            if (score_manager.score % 10 == 0 and score_manager.score != last_incremented_score):
                clock_speed += 1
                last_incremented_score = score_manager.score

        clock.tick(clock_speed)

if __name__ == "__main__":
    main()