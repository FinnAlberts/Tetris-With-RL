# Import pygame
import pygame
import constants
import random
import copy

# Create a block class
class Block:
    # Initiailize Block
    def __init__(self, x_position = 5.0, y_position = 0.0):
        self.x_position = x_position * constants.BLOCK_SIZE
        self.y_position = y_position * constants.BLOCK_SIZE
        self.block_color = (255, 0, 0)

    # Get x position
    def get_x_in_blocks(self):
        return int(self.x_position // constants.BLOCK_SIZE)

    # Get y position
    def get_y_in_pixels(self):
        return self.y_position

    def get_y_in_blocks(self):
        return int(self.y_position // constants.BLOCK_SIZE)

    # Check if block can move left
    def can_move_left(self, field):
        if self.get_x_in_blocks() > 0:
            if field[self.get_y_in_blocks()][self.get_x_in_blocks() - 1] == 0:
                return True
        return False

    # Move left
    def move_left(self):
        self.x_position -= 1 * constants.BLOCK_SIZE
        if self.x_position < 0:
            self.x_position = 0

    # Check if block can move right
    def can_move_right(self, field):
        if self.get_x_in_blocks() < 9:
            if field[self.get_y_in_blocks()][self.get_x_in_blocks() + 1] == 0:
                return True
        return False

    # Move right
    def move_right(self):
        self.x_position += 1 * constants.BLOCK_SIZE
        if self.x_position > 9 * constants.BLOCK_SIZE:
            self.x_position = 9 * constants.BLOCK_SIZE

    # Check if block can move down
    def can_move_down(self, field):
        if self.get_y_in_blocks() < 19:
            if field[self.get_y_in_blocks() + 1][self.get_x_in_blocks()] == 0:
                return True
        return False
    
    # Fall down
    def fall_down(self, fall_speed, delta_time):
        self.y_position += fall_speed * delta_time / 1000

    # Set y position
    def set_y(self, y_position):
        self.y_position = y_position

# Create a Tetronimo class
class Tetronimo:
    # Initialize Tetronimo
    def __init__(self):
        self.blocks = []
        # Choose a random tetronimo
        tetronimo_type = random.randint(0, 1)
        # Create a tetronimo
        # Straight shape
        if tetronimo_type == 0:
            for i in range(4):
                self.blocks.append(Block(3 + i, 0))
        # Square shape
        elif tetronimo_type == 1:
            self.blocks.append(Block(4, 0))
            self.blocks.append(Block(5, 0))
            self.blocks.append(Block(4, 1))
            self.blocks.append(Block(5, 1))

    def get_blocks(self):
        return self.blocks
    
    # Move the tetronimo to the left if possible
    def move_left(self, field):
        # Check if Tetronimo can move left
        for block in self.blocks:
            if block.can_move_left(field) == False:
                return

        # Move the block left
        for block in self.blocks:
            block.move_left()

    # Move the tetronimo to the left if possible
    def move_right(self, field):
        # Check if Tetronimo can move right
        for block in self.blocks:
            if block.can_move_right(field) == False:
                return
        
        # Move the block right
        for block in self.blocks:
            block.move_right()

    # Check if tetronimo can move down
    def can_move_down(self, field):
        for block in self.blocks:
            if block.can_move_down(field) == False:
                return False
        return True

    # Move the tetronimo down 
    def fall_down(self, fall_speed, delta_time):
        for block in self.blocks:
            block.fall_down(fall_speed, delta_time)      


# Update runs once per frame
def update():
    global fall_speed
    global clock
    global field
    global tetronimo
    global score

    for event in pygame.event.get():
        # Check if the game is quit
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Check if the user pressed a key
        if event.type == pygame.KEYDOWN:
            # Left movement
            if event.key == pygame.K_LEFT:
                tetronimo.move_left(field)
            # Right movement
            if event.key == pygame.K_RIGHT:
                tetronimo.move_right(field)

    # Check for full rows
    score += check_for_full_rows(field)

    # Check if the game is over
    if is_game_over(field):
        print("Game over")
        return

    # Get delta time
    delta_time = clock.tick(constants.FPS)

    # Check if tetronimo can move down
    if tetronimo.can_move_down(field):
        tetronimo.fall_down(fall_speed, delta_time)
    else:
        # Set the tetronimo to the field
        for block in tetronimo.get_blocks():
            field[block.get_y_in_blocks()][block.get_x_in_blocks()] = 1
        # Create a new tetronimo
        tetronimo = Tetronimo()

    # Draw the screen
    draw_screen(field, tetronimo)    

    # Update the screen
    pygame.display.update()

# Draw the screen (includes field, current tetronimo and background)
def draw_screen(field, current_tetronimo):
    # Fill the screen with black
    window.fill((0, 0, 0))

    # Make the playing field dark gray
    pygame.draw.rect(window, (50, 50, 50), (0, 0, 10 * constants.BLOCK_SIZE, 20 * constants.BLOCK_SIZE))

    # Draw every block in the field
    for y in range(20):
        for x in range(10):
            if field[y][x] == 1:
                pygame.draw.rect(window, (0, 255, 0), (x * constants.BLOCK_SIZE, y * constants.BLOCK_SIZE, constants.BLOCK_SIZE, constants.BLOCK_SIZE))

    # Draw the current tetronimo
    for block in current_tetronimo.get_blocks():
        pygame.draw.rect(window, block.block_color, (block.get_x_in_blocks() * constants.BLOCK_SIZE, block.get_y_in_blocks() * constants.BLOCK_SIZE, constants.BLOCK_SIZE, constants.BLOCK_SIZE))

    # Draw the score
    font = pygame.font.Font('freesansbold.ttf', 25)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (10 * constants.BLOCK_SIZE + 20 , 40))

# Check the field for full rows
def check_for_full_rows(field):
    # Check if there are full rows
    full_rows = 0
    for y in range(20):
        full = True
        for x in range(10):
            if field[y][x] == 0:
                full = False
        if full:
            full_rows += 1
            # Remove the full row
            for x in range(10):
                field[y][x] = 0
            # Move all rows above down
            for y2 in range(y, 1, -1):
                for x2 in range(10):
                    field[y2][x2] = field[y2 - 1][x2]
    return full_rows

# Check if the game is over (block in the top row)
def is_game_over(field):
    for x in range(10):
        if field[0][x] == 1:
            return True
    return False

# Reset the game
def reset():
    global field
    global tetronimo
    global score
    field = [[0 for x in range(10)] for y in range(20)]
    tetronimo = Tetronimo()
    score = 0

# Initialize the game
def initialize_game():
    global window
    global clock
    global field
    global tetronimo
    global score
    global fall_speed

    # Initialize pygame
    pygame.init()

    # Create a pygame window
    window = pygame.display.set_mode((10 * constants.BLOCK_SIZE + 200, 20 * constants.BLOCK_SIZE))
    pygame.display.set_caption("Tetris")

    # Create a clock
    clock = pygame.time.Clock()

    fall_speed = 160 # Default = 40, set higher for debugging
    score = 0
    tetronimo = Tetronimo()

    # Generate a 2D list of 0s to represent the playing field
    field = [[0 for x in range(10)] for y in range(20)]

# Get current gamestate
def get_gamestate():
        global field
        global score
        global tetronimo

        # Create a dictionary with the gamestate
        gamestate = {}

        # Add the field to the dictionary
        field_with_current_tetronimo = copy.deepcopy(field)

        # Add the current tetronimo to the field
        for block in tetronimo.get_blocks():
            # Safety check for out of bounds
            if block.get_y_in_blocks() < 20 and block.get_x_in_blocks() < 10:
                field_with_current_tetronimo[block.get_y_in_blocks()][block.get_x_in_blocks()] = 1
        gamestate['field'] = field_with_current_tetronimo

        # Add the score to the dictionary
        gamestate['score'] = score

        gamestate['is_game_over'] = is_game_over(field)

        # Return the dictionary
        return gamestate

if __name__ == "__main__":
    # Run the game
    initialize_game()

    run = True
    while run:
        update()