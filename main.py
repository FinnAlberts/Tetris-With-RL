import time
from environment import TetrisEnvironment
import os
from stable_baselines3 import PPO

TIMESTAMPS = 10000
EPISODES = 100

# Function for training the model and running the game
def main():
    print("START TRAINING")
    # Register Gym environment and create model
    gym.register('Tetris-v0', entry_point=TetrisEnvironment)
# Declare folder paths
models_directory = f"models/PPO{int(time.time())}"
log_directory = f"logs/PPO{int(time.time())}"

# Create folders if they do not yet exist
if not os.path.exists(models_directory):
    os.makedirs(models_directory)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Create environment
environment = TetrisEnvironment()
environment.reset()

model = PPO("MlpPolicy", environment, verbose=1, tensorboard_log=log_directory)

# Run the program for a set amount of episodes
for episode in range(1, EPISODES + 1):
    model.learn(total_timesteps=TIMESTAMPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_directory}/PPO{episode * TIMESTAMPS}")