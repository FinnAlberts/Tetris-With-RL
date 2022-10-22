import gym
from environment import TetrisEnvironment
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from os import path


# Function for training the model and running the game
def main():
    print("START TRAINING")
    # Register Gym environment and create model
    gym.register('Tetris-v0', entry_point=TetrisEnvironment)


    # Run the program infinitely
    while True:
        # Learn for 20 000 steps
        # model.learn(20000)

        # Save the model
        print("Saving the model to trained_model.zip")
        # model.save("trained_model.zip")



