import pygame
import Constants as C
import random
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource for dev and for PyInstaller bundle."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Fruit:
    def __init__(self,snake=None, obstacles=None):
        self.snake = snake
        self.obstacles = obstacles

        #Load fruit image
        self.image = pygame.image.load(resource_path(os.path.join('images','fruit.png')))
        #scale image to fit cell size
        self.image = pygame.transform.scale(self.image, (C.CELL_SIZE+5,C.CELL_SIZE+5))
        self.position = self.spawn()

    def spawn(self):
        """Spawn the fruit at a random position on the grid."""

        # Keep generating random positions until we find one that doesn't collide with the snake
        while True:

            x = random.randint(1, (C.GRID_WIDTH // C.CELL_SIZE) -2) * C.CELL_SIZE + C.GRID_OFFSET_X
            y = random.randint(1, (C.GRID_HEIGHT // C.CELL_SIZE) -2) * C.CELL_SIZE + C.GRID_OFFSET_Y
            new_position = (x, y)

            # Check if the fruit spawned on the snake's body or an obstacle
            valid_position = True
            if self.snake and new_position in self.snake.body:
                valid_position = False
            if self.obstacles and new_position in self.obstacles:
                valid_position = False

            if valid_position:
                return new_position

    def draw(self, screen):
        """Draw the fruit on the screen."""
        screen.blit(self.image, self.position)