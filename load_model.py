from stable_baselines3 import PPO
from environment import TetrisEnvironment

# Create the environment
environment = TetrisEnvironment()

# Load the model
models_directory = "models"
model_name = str(input("Enter the name of the model you want to load (e.g. PPO1666441418/PPO1000000.zip): "))
model_path = f"{models_directory}/{model_name}"
model = PPO.load(model_path, env=environment)

# Run the model
episodes = 5
for episode in range(episodes):
    observation = environment.reset()
    done = False
    while not done:
        action, _states = model.predict(observation)
        observation, rewards, done, info = environment.step(action)
        environment.render()