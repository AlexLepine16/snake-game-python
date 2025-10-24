import pygame
import Constants as C

class Snake:
    def __init__(self):
        self.reset() 
        self.color = C.GREEN #this is the default color of the snake
        self.eye_radius = 2 #size of the snake's eyes
        self.eye_offset = C.CELL_SIZE//4 # distance from the edges

    def reset(self):
        """Reset the snake to its initial state."""
        self.body = [(C.GRID_OFFSET_X + C.GRID_WIDTH // 2, C.GRID_OFFSET_Y + C.GRID_HEIGHT // 2)]
        self.direction = "RIGHT"
        self.new_direction = "RIGHT"

    def move(self,grow=False):
        """Update the snake's position based on the current direction."""
        
        # Update the direction based on the buffered input
        self.direction = self.new_direction

        # Calculate the new head position
        x, y = self.body[0]
        if self.direction == "UP":
            y -= C.CELL_SIZE
        elif self.direction == "DOWN":
            y += C.CELL_SIZE
        elif self.direction == "LEFT":
            x -= C.CELL_SIZE
        elif self.direction == "RIGHT":
            x += C.CELL_SIZE

        # Insert the new head position at the beginning of the body
        self.body.insert(0, (x, y))

        # Remove the tail segment (unless the snake is growing)
        if not grow:    
            self.body.pop()

    def change_direction(self, new_direction):
        #Change the snake's direction making usre it can't go in the opposite direction
        if (new_direction == "UP" and self.direction != "DOWN") or \
           (new_direction == "DOWN" and self.direction != "UP") or \
           (new_direction == "LEFT" and self.direction != "RIGHT") or \
           (new_direction == "RIGHT" and self.direction != "LEFT"):
            self.new_direction = new_direction

    def check_collision(self, obstacles=None):
        """Check if the snake collides with the grid boundaries or itself."""
        x, y = self.body[0]

        
        # Check grid boundaries
        if x < C.GRID_OFFSET_X or x >= C.GRID_OFFSET_X + C.GRID_WIDTH or y < C.GRID_OFFSET_Y or y >= C.GRID_OFFSET_Y + C.GRID_HEIGHT:
            return True

        # Check self-collision (head collides with any body segment)
        if self.body[0] in self.body[1:]:
            return True
        
        #Check obstacle collision
        if obstacles and self.body[0] in obstacles:
            return True

        # Return False if no collision
        return False

    def draw(self, screen):
        """Draw the snake on the screen."""
        for i, segment in enumerate(self.body):
            pygame.draw.rect(screen, self.color, (*segment, C.CELL_SIZE, C.CELL_SIZE))

            # Draw the eyes on the head segment
            if i == 0:
                self.draw_eyes(screen, segment)

    def draw_eyes(self, screen, head_pos):
        """Draw eyes on the snake's head.  They are drawn in the direction of movement."""

        #Determine the eye color depending on the snake color
        eye_color = C.RED if self.color == C.BLACK else C.BLACK

        # Calculate the eye positions based on the direction
        x, y = head_pos
        if self.direction == "RIGHT":
            eye1 = (x + C.CELL_SIZE - self.eye_offset, y + self.eye_offset)
            eye2 = (x + C.CELL_SIZE - self.eye_offset, y + C.CELL_SIZE - self.eye_offset)
        elif self.direction == "LEFT":
            eye1 = (x + self.eye_offset, y + self.eye_offset)
            eye2 = (x + self.eye_offset, y + C.CELL_SIZE - self.eye_offset)
        elif self.direction == "UP":
            eye1 = (x + self.eye_offset, y + self.eye_offset)
            eye2 = (x + C.CELL_SIZE - self.eye_offset, y + self.eye_offset)
        else:  # DOWN
            eye1 = (x + self.eye_offset, y + C.CELL_SIZE - self.eye_offset)
            eye2 = (x + C.CELL_SIZE - self.eye_offset, y + C.CELL_SIZE - self.eye_offset)

        # Draw the eyes
        pygame.draw.circle(screen, eye_color, eye1, self.eye_radius)
        pygame.draw.circle(screen, eye_color, eye2, self.eye_radius)