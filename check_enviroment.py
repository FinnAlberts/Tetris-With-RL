# This is a script for checking the environment by executing random actions
# The action, observation and reward variables are printed to the console

from environment import TetrisEnvironment

environment = TetrisEnvironment()
episodes = 50

for episode in range(episodes):
    done = False
    observation = environment.reset()
    while True:
        random_action = environment.action_space.sample()
        print("action", random_action)
        obs, reward, done, info = environment.step(random_action)
        print('observation', obs)
        print('reward', reward)