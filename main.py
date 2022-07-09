import gym
from environment import TetrisEnvironment
from stable_baselines3 import PPO
from os import path
from graph import graph
from multiprocessing import Process

# Function for running graph.py and main.py simultaneously
def run_in_parallel(*fns):
  processes = []
  for fn in fns:
    process = Process(target=fn)
    process.start()
    processes.append(process)
  for process in processes:
    process.join()

# Function for training the model and running the game
def main():
    print("START TRAINING")
    # Register Gym environment and create model
    gym.register('Tetris-v0', entry_point=TetrisEnvironment)
    model = PPO('MlpPolicy', 'Tetris-v0')

    # Check if a model already exists and if so load it
    if path.exists("trained_model.zip"):
        model.load("trained_model.zip")

    # Run the program infinitely
    while True:
        # Learn for 20 000 steps
        model.learn(20000)

        # Save the model
        print("Saving the model to trained_model.zip")
        model.save("trained_model.zip")


if __name__ == "__main__":
    print("HI WORLD IM ALIVE")
    run_in_parallel(main, graph)
