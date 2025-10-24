import pygame  
import Constants as C  
import random  

class Obstacle:  
    def __init__(self, snake=None):  
        self.snake = snake  
        self.obstacles = []  
        self.color = C.GREY

    def spawn(self, additional=False):  
        """Spawn obstacles (1 horizontal 1x3, 1 vertical 3x1)."""  
        if not additional:
            self.obstacles = []  

        # Spawn horizontal obstacle
        if not additional:
            while True:  
                x = random.randint(1, (C.GRID_WIDTH // C.CELL_SIZE) - 3) * C.CELL_SIZE + C.GRID_OFFSET_X  
                y = random.randint(1, (C.GRID_HEIGHT // C.CELL_SIZE) - 1) * C.CELL_SIZE + C.GRID_OFFSET_Y  
                horizontal = [(x, y), (x + C.CELL_SIZE, y),(x + 2 * C.CELL_SIZE, y)]  

                if not self.snake or all(pos not in self.snake.body for pos in horizontal):  
                    self.obstacles.extend(horizontal)  
                    break  

        # spawn vertical obstacle
        if not additional:
            while True:  
                x = random.randint(1, (C.GRID_WIDTH // C.CELL_SIZE) - 1) * C.CELL_SIZE + C.GRID_OFFSET_X  
                y = random.randint(1, (C.GRID_HEIGHT // C.CELL_SIZE) - 3) * C.CELL_SIZE + C.GRID_OFFSET_Y  
                vertical = [(x, y), (x, y + C.CELL_SIZE), (x, y + 2 * C.CELL_SIZE)]  

                if (not self.snake or all(pos not in self.snake.body for pos in vertical)) and all(pos not in self.obstacles for pos in vertical):  
                    self.obstacles.extend(vertical)  
                    break  
        
        else:
            # Spawn additional obstacle (choose between horizontal and vertical randomly)
            obstacle_type = random.choice(['horizontal', 'vertical'])
            if obstacle_type == 'horizontal':
                while True:  
                    x = random.randint(1, (C.GRID_WIDTH // C.CELL_SIZE) - 3) * C.CELL_SIZE + C.GRID_OFFSET_X  
                    y = random.randint(1, (C.GRID_HEIGHT // C.CELL_SIZE) - 1) * C.CELL_SIZE + C.GRID_OFFSET_Y  
                    new_obstacle = [(x, y), (x + C.CELL_SIZE, y),(x + 2 * C.CELL_SIZE, y)]

                    if (not self.snake or all(pos not in self.snake.body for pos in new_obstacle)) and all(pos not in self.obstacles for pos in new_obstacle):
                        self.obstacles.extend(new_obstacle)
                        break
            else:
                while True:  
                    x = random.randint(1, (C.GRID_WIDTH // C.CELL_SIZE) - 1) * C.CELL_SIZE + C.GRID_OFFSET_X  
                    y = random.randint(1, (C.GRID_HEIGHT // C.CELL_SIZE) - 3) * C.CELL_SIZE + C.GRID_OFFSET_Y  
                    new_obstacle = [(x, y), (x, y + C.CELL_SIZE), (x, y + 2 * C.CELL_SIZE)]

                    if (not self.snake or all(pos not in self.snake.body for pos in new_obstacle)) and all(pos not in self.obstacles for pos in new_obstacle):
                        self.obstacles.extend(new_obstacle)
                        break

    def draw(self, screen):  
        #Draw the obstacles on the screen  
        for pos in self.obstacles:  
            pygame.draw.rect(screen, self.color, (*pos, C.CELL_SIZE, C.CELL_SIZE))  