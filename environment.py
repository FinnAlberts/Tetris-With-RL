import gym
from gym import spaces
import tetris
from pynput.keyboard import Key, Controller
FPS = 30
BLOCK_SIZE = 25
FALL_SPEED = 300 # Default = 40, set higher for debugging

class TetrisEnvironment(gym.Env):
    def __init__(self):
        super().__init__()

        # Define action space (do nothing, left, right)
        self.action_space = spaces.Discrete(3)

        # Define observation space
        self.observation_space = spaces.Box(low=0, high=2, shape=(20, 10))

        # Initialize pynput controller for giving input
        self.keyboard = Controller()

        # Initialize tetris game
        tetris.initialize_game()
        print("Gym environment initialized")

    def step(self, action: int):
        # Give input
        self.give_input(action)

        # Read gamestate
        gamestate = tetris.get_gamestate()

        # Get observation
        observation = gamestate['field']

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

        # Check if done
        if done:
            # Print total reward
            print("Reward is", self.total_reward)

            # Log total reward
            with open('rewards.txt', 'a', encoding='utf-8') as file:
                file.write(str(self.total_reward) + " " + str(gamestate['score']) + "\n")

        # Create info dictionary
        info = {}

        # Update game
        tetris.update()

        # Increase step counter
        self.step_counter += 1

        # Return observation, reward, done, info
        return observation, reward, done, info

    def give_input(self, action):
        self.keyboard.release(Key.left)
        self.keyboard.release(Key.right)

        # Move left
        if action == 1:
            self.keyboard.press(Key.left)
        # Move right
        elif action == 2:
            self.keyboard.press(Key.right)

    def get_reward(self, gamestate, action):
        # Get reward
        reward = 0

        # Check if game is over
        if gamestate['is_game_over']:
            reward -= 250

        # Check if score has increased
        reward += (gamestate['score'] - self.score) * 100

        # Check if tetronimo has moved left or right
        if action == 1 or action == 2:
            reward -= 0.1
    
        return reward

    def reset(self):
        # Reset step counter
        self.step_counter = 0

        # Reset score
        self.score = 0

        # Reset total reward
        self.total_reward = 0

        # Reset game
        tetris.reset()

        # Read gamestate
        gamestate = tetris.get_gamestate()

        # Get observation
        observation = gamestate['field']

        # Set input to none
        self.give_input(0)

        # Return observation
        return observation

    def render(self, mode='human', close=False):
        return None