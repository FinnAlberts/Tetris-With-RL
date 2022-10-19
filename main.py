import gym
from environment import TetrisEnvironment
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
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

    # Check if a model already exists and if so load it
    if path.exists("trained_model.zip"):
        model = PPO.load("trained_model.zip")
    else:
        model = PPO('MlpPolicy', 'Tetris-v0', verbose=1)

    # Run the program infinitely
    while True:
        # Learn for 20 000 steps
        # model.learn(20000)

        # Save the model
        print("Saving the model to trained_model.zip")
        # model.save("trained_model.zip")

        # Try out trained model
        environment = TetrisEnvironment()
        obs = environment.reset()
        for i in range(100000):
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = environment.step(action)
            if done:
              obs = environment.reset()

        environment.close()


if __name__ == "__main__":
    print("HI WORLD IM ALIVE")
    run_in_parallel(main, graph)
