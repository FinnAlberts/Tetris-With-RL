import time
from environment import TetrisEnvironment
import os
from stable_baselines3 import PPO


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

    # Run the program infinitely
    while True:
        # Learn for 20 000 steps
        # model.learn(20000)

        # Save the model
        print("Saving the model to trained_model.zip")
        # model.save("trained_model.zip")



