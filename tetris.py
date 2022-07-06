# Import pygame
import pygame
import constants

# Create a block class
class Block:
    # Initiailize Block
    def __init__(self):
        self.x_position = 5
        self.y_position = 0.0
        self.block_color = (255, 0, 0)

    # Get x position
    def get_x_in_blocks(self):
        return self.x_position

    # Get y position
    def get_y_in_pixels(self):
        return self.y_position

    def get_y_in_blocks(self):
        return self.y_position // constants.BLOCK_SIZE

    # Move left
    def move_left(self):
        self.x_position -= 1
        if self.x_position < 0:
            self.x_position = 0

    # Move right
    def move_right(self):
        self.x_position += 1
        if self.x_position > 9:
            self.x_position = 9
    
    # Fall down
    def fall_down(self, fall_speed, delta_time):
        self.y_position += fall_speed * delta_time / 1000

    # Set y position
    def set_y(self, y_position):
        self.y_position = y_position

# Update runs once per frame
def update():
    global y_position
    global x_position
    global y_speed
    global clock
    global field
    global block

    # Check if game is quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                block.move_left()
            if event.key == pygame.K_RIGHT:
                block.move_right()

    # Reset the screen
    reset_screen()

    # Get delta time
    delta_time = clock.tick(constants.FPS)

    # Let the block fall
    block.fall_down(y_speed, delta_time)

    if block.get_y_in_blocks() > 20:
        block.set_y(0)

    # Draw a red cube of 25 by 25 pixels on the screen
    pygame.draw.rect(window, (255, 0, 0), (block.get_x_in_blocks() * constants.BLOCK_SIZE, block.get_y_in_blocks() * constants.BLOCK_SIZE, 25, 25))

    # Update the screen
    pygame.display.update()

    # Print current position of block in blocks
    print(block.get_x_in_blocks(), block.get_y_in_blocks())

# Reset the screen so it shows a black background with a gray playing field
def reset_screen():
    # Fill the screen with black
    window.fill((0, 0, 0))

    # Make the playing field dark gray
    pygame.draw.rect(window, (50, 50, 50), (0, 0, 10 * constants.BLOCK_SIZE, 20 * constants.BLOCK_SIZE))
    
# Initialize pygame
pygame.init()

# Create a pygame window
window = pygame.display.set_mode((10 * constants.BLOCK_SIZE + 200, 20 * constants.BLOCK_SIZE))
pygame.display.set_caption("Tetris")

# Create a clock
clock = pygame.time.Clock()

y_speed = 40
block = Block()

# Generate a 2D list of 0s to represent the playing field
field = [[0 for x in range(10)] for y in range(20)]
print(field)

run = True
while run:
    update()