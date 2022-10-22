from environment import TetrisEnvironment

env = TetrisEnvironment()
episodes = 50

for episode in range(episodes):
    done = False
    obs = env.reset()
    while True:#not done:
        random_action = env.action_space.sample()
        print("action", random_action)
        obs, reward, done, info = env.step(random_action)
        print('obs', obs)
        print('reward', reward)