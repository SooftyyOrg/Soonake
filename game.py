import pygame
import random
import os

# Initialize pygame
pygame.init()

# Set up the display
block_size = 30
board_width = 23
board_height = 20
screen_width = block_size * board_width
screen_height = block_size * board_height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Define the Snake class
class Snake:
    def __init__(self):
        # Initialize the snake at the center of the board
        self.body = [(board_width // 2, board_height // 2)]
        # Set initial movement direction
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    
    def move(self):
        # Move the snake in the current direction
        head = self.body[0]
        x, y = head
        if self.direction == 'UP':
            y -= 1
        elif self.direction == 'DOWN':
            y += 1
        elif self.direction == 'LEFT':
            x -= 1
        elif self.direction == 'RIGHT':
            x += 1
        # Update the snake's body with the new position
        self.body.insert(0, (x, y))
        self.body.pop()
    
    def grow(self):
        # Increase the snake's length by adding a new segment at the tail
        tail = self.body[-1]
        x, y = tail
        if self.direction == 'UP':
            y += 1
        elif self.direction == 'DOWN':
            y -= 1
        elif self.direction == 'LEFT':
            x += 1
        elif self.direction == 'RIGHT':
            x -= 1
        # Add the new segment to the end of the snake's body
        self.body.append((x, y))
    
    def draw(self):
        # Draw the snake on the screen
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(screen, green, (x * block_size, y * block_size, block_size, block_size))

# Define the Food class
class Food:
    def __init__(self):
        # Initialize the food at a random position on the board
        self.x = random.randint(0, board_width - 1)
        self.y = random.randint(0, board_height - 1)
    
    def draw(self):
        # Draw the food on the screen
        pygame.draw.rect(screen, red, (self.x * block_size, self.y * block_size, block_size, block_size))

# Define the game over screen function
def game_over_screen(reason):
    font = pygame.font.SysFont(None, 50)
    reason_text = font.render(reason, True, white)
    retry_text = font.render("Press 'R' to try again", True, white)
    # Display the game over message and retry instructions
    screen.blit(reason_text, (screen_width // 2 - reason_text.get_width() // 2, screen_height // 2 - 50))
    screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.update()

# Define functions for handling high scores
def save_high_score(score):
    # Create the directory if it doesn't exist
    directory = os.path.expanduser("~/Documents/sooftyy/snake")
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Write the high score to the file
    highscore_file = os.path.join(directory, "highscore.txt")
    with open(highscore_file, "w") as file:
        file.write(str(score))

def load_high_score():
    # Load the high score from the file, or return 0 if it doesn't exist
    directory = os.path.expanduser("~/Documents/sooftyy/snake")
    highscore_file = os.path.join(directory, "highscore.txt")
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as file:
            return int(file.read())
    else:
        return 0

def update_high_score(score):
    # Load the current high score
    old_high_score = load_high_score()
    # If the current score is higher than the old high score, update the high score
    if score > old_high_score:
        save_high_score(score)

# Define the main function
def main():
    # Initialize variables
    snake = Snake()
    food = Food()
    clock = pygame.time.Clock()
    running = True
    game_over = False
    score = 0
    high_score = load_high_score()

    while running:
        if game_over:
            # Check if the player's score is higher than the current high score
            if score > high_score:
                # Update the high score if needed
                update_high_score(score)
                # Reload the high score after updating
                high_score = load_high_score()
            
            # Display game over screen and handle events
            game_over_screen("Game Over! Score: {} High Score: {}".format(score, high_score))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart the game if 'R' key is pressed
                        snake = Snake()
                        food = Food()
                        score = 0
                        game_over = False
        else:
            # Clear the screen
            screen.fill(black)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Change snake direction based on arrow keys
                    if event.key == pygame.K_UP and snake.direction != 'DOWN':
                        snake.direction = 'UP'
                    elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                        snake.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                        snake.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                        snake.direction = 'RIGHT'
            
            # Check for collision with food
            if snake.body[0] == (food.x, food.y):
                # Grow the snake, update score, and spawn new food
                snake.grow()
                food = Food()
                score += 1
                save_high_score(score)
            
            # Check for collision with walls
            head = snake.body[0]
            if head[0] < 0 or head[0] >= board_width or head[1] < 0 or head[1] >= board_height:
                # End the game if the snake hits a wall
                game_over = True
                continue
            
            # Check for collision with itself
            if len(snake.body) != len(set(snake.body)):
                # End the game if the snake collides with itself
                game_over = True
                continue
            
            # Move the snake, draw it on the screen, and draw the food
            snake.move()
            snake.draw()
            food.draw()
            
            # Update the display and control the game speed
            pygame.display.update()
            clock.tick(10)

    # Quit pygame when the game loop ends
    pygame.quit()

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()