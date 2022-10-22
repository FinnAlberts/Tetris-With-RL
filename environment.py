import copy
import gym
from gym import spaces
import pygame
import numpy

FPS = 30
BLOCK_SIZE = 25
FALL_SPEED = 300 # Default = 40, set higher for debugging

# Create a block class
class Block:
    # Initiailize Block
    def __init__(self, x_position = 5.0, y_position = 0.0):
        self.x_position = x_position * BLOCK_SIZE
        self.y_position = y_position * BLOCK_SIZE
        self.block_color = (255, 0, 0)

    # Get x position
    def get_x_in_blocks(self):
        if self.x_position // BLOCK_SIZE < 0:
            return 0
        if self.x_position // BLOCK_SIZE > 9:
            return 9
        return int(self.x_position // BLOCK_SIZE)

    # Get y position
    def get_y_in_pixels(self):
        return self.y_position

    def get_y_in_blocks(self):
        if self.y_position // BLOCK_SIZE < 0:
            return 0
        if self.y_position // BLOCK_SIZE > 19:
            return 19
        return int(self.y_position // BLOCK_SIZE)

    # Check if block can move left
    def can_move_left(self, field):
        if self.get_x_in_blocks() > 0:
            if field[self.get_y_in_blocks()][self.get_x_in_blocks() - 1] == 0:
                return True
        return False

    # Move left
    def move_left(self):
        self.x_position -= 1 * BLOCK_SIZE
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
        self.x_position += 1 * BLOCK_SIZE
        if self.x_position > 9 * BLOCK_SIZE:
            self.x_position = 9 * BLOCK_SIZE

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
        tetronimo_type = 3
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
        # Single 1x1 block
        elif tetronimo_type == 3:
            self.blocks.append(Block(4, 0))

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

class TetrisEnvironment(gym.Env):
    def __init__(self):
        super().__init__()

        # Define action space (do nothing, left, right)
        self.action_space = spaces.Discrete(3)

        # Define observation space
        self.observation_space = spaces.Box(low=0, high=20, shape=(12,), dtype=numpy.float32)

    def step(self, action: int):
        # Game handling
        for event in pygame.event.get():
            # Check if the game is quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Left movement
        if action == 1:
            self.tetronimo.move_left(self.field)
        # Right movement
        if action == 2:
            self.tetronimo.move_right(self.field)

        # Check for full rows
        self.score += check_for_full_rows(self.field)

        # Check if the game is over
        if is_game_over(self.field):
            done = True

        # Get delta time
        delta_time = self.clock.tick(FPS)

        # Check if tetronimo can move down
        if self.tetronimo.can_move_down(self.field):
            self.tetronimo.fall_down(self.fall_speed, delta_time)
        else:
            # Set the tetronimo to the field
            for block in self.tetronimo.get_blocks():
                self.field[block.get_y_in_blocks()][block.get_x_in_blocks()] = 1
            # Create a new tetronimo
            self.tetronimo = Tetronimo()

        # Draw the screen
        self.draw_screen()    

        # Update the screen
        pygame.display.update()

        # Read gamestate
        gamestate = self.get_gamestate()

        # Get observation
        field = gamestate['field']

        # Build observation, based on height and position of current tetronimo and height of each column of the field
        observation = []
        observation.append(self.tetronimo.get_blocks()[0].get_y_in_blocks())
        observation.append(self.tetronimo.get_blocks()[0].get_x_in_blocks())
        for x in range(10):
            for y in range(20):
                if field[y][x] == 1:
                    observation.append(y)
                    break
                if y == 19:
                    observation.append(20)

        # Get reward
        reward = self.get_reward(gamestate, action)
        self.total_reward += reward

        # Update current score
        self.score = gamestate['score']

        # Check if game is over
        if gamestate['is_game_over']:
            done = True
        else:
            done = False

        # Create info dictionary
        info = {}

        # Return observation, reward, done, info
        return observation, reward, done, info

    def get_reward(self, gamestate, action):
        # Get reward
        reward = 0

        # Check if game is over
        if gamestate['is_game_over']:
            reward -= 250

        # Check if score has increased
        reward += (gamestate['score'] - self.score) * 100

        # Get a reward for height of the tetronimo
        reward += (gamestate['average_height_of_current_tetronimo'])

        # Check if tetronimo has moved left or right
        if action == 1 or action == 2:
            reward -= 0.1
    
        return reward

    def reset(self):
        # Reset total reward
        self.total_reward = 0

        # Initialize pygame
        pygame.init()

        # Create a pygame window
        self.window = pygame.display.set_mode((10 * BLOCK_SIZE + 200, 20 * BLOCK_SIZE))
        pygame.display.set_caption("Tetris")

        # Create a clock
        self.clock = pygame.time.Clock()

        self.fall_speed = FALL_SPEED 
        self.score = 0
        self.tetronimo = Tetronimo()

        # Generate a 2D list of 0s to represent the playing field
        self.field = [[0 for x in range(10)] for y in range(20)]

        # Read gamestate
        gamestate = self.get_gamestate()

        # Get observation
        field = gamestate['field']

        # Build observation, based on height and position of current tetronimo and height of each column of the field
        observation = []
        observation.append(self.tetronimo.get_blocks()[0].get_y_in_blocks())
        observation.append(self.tetronimo.get_blocks()[0].get_x_in_blocks())
        for x in range(10):
            for y in range(20):
                if field[y][x] == 1:
                    observation.append(y)
                    break
                if y == 19:
                    observation.append(20)

        # Return observation
        return observation

    # Get current gamestate
    def get_gamestate(self):
        # Create a dictionary with the gamestate
        gamestate = {}

        # Add the field to the dictionary
        field_with_current_tetronimo = copy.deepcopy(self.field)

        # Add the current tetronimo to the field
        for block in self.tetronimo.get_blocks():
            field_with_current_tetronimo[block.get_y_in_blocks()][block.get_x_in_blocks()] = 2
        gamestate['field'] = field_with_current_tetronimo

        # Add the score to the dictionary
        gamestate['score'] = self.score

        # Add game over state to the dictionary
        gamestate['is_game_over'] = is_game_over(self.field)

        # Add avarage height of current tetronimo to the dictionary
        average_height = 0
        for block in self.tetronimo.get_blocks():
            average_height += block.get_y_in_blocks()
        gamestate['average_height_of_current_tetronimo'] = average_height / len(self.tetronimo.get_blocks())

        # Return the dictionary
        return gamestate

    # Draw the screen (includes field, current tetronimo and background)
    def draw_screen(self):
        # Fill the screen with black
        self.window.fill((0, 0, 0))

        # Make the playing field dark gray
        pygame.draw.rect(self.window, (50, 50, 50), (0, 0, 10 * BLOCK_SIZE, 20 * BLOCK_SIZE))

        # Draw every block in the field
        for y in range(20):
            for x in range(10):
                if self.field[y][x] == 1:
                    pygame.draw.rect(self.window, (0, 255, 0), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Draw the current tetronimo
        for block in self.tetronimo.get_blocks():
            pygame.draw.rect(self.window, block.block_color, (block.get_x_in_blocks() * BLOCK_SIZE, block.get_y_in_blocks() * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Draw the score
        font = pygame.font.Font('freesansbold.ttf', 25)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.window.blit(score_text, (10 * BLOCK_SIZE + 20 , 40))

    def render(self, mode='human', close=False):
        return None