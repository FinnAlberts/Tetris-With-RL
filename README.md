# Tetris with reinforcement learning
This repository contains Tetris with reinforcement learning. The game is written in Python and the reinforcement learning is done with stable-baselines3. Some pretrained models are included in the models folder.

The used Tetris game is custom made and is not based on any other Tetris game. The game is written in Python and uses Pygame for the graphics. The game is simplified to improve the perforamnce of the reinforcement learning. This is done by only having 1x1 blocks falling instead of the regular shapes.

## Getting started
The application exists of three parts:
- The training script for training a model
- The loading script for loading a trained model

To install necessary packages run:

```pip install -r requirements.txt```

### Training
To train a model, run the following command:

```python train_model.py```

The model will train for 100 episodes of 10 000 steps each. After each episode, the model will be saved to the models folder.

### Loading
To load a model, run the following command:

```python load_model.py```

The model will load the model from the models folder and play the game for 5 episodes. Model names are defined as follows: ```{used_algorithm}{timestamp}_{used_algorithm}{number_of_timestamps_trained}.zip```

## Viewing the progress using Tensorboard
It is possible to view the results of the training using Tensorboard. To do this, run the following command:

```python -m tensorboard.main --logdir=logs```

After TensorBoard has started, open a browser and go to ```http://localhost:6006/```.

## Customizing the environment
It is possible to customize the environment by changing the ```enviroment.py``` file. One of the easiest ways to change the environment is changing the reward function. The reward function is defined in ```get_reward(...)```.

Is is also possible to change the used algorithm by changing the ```train_model.py``` file. To do this, replace all instances of ```PPO``` (in lines 4, 10, 11, 23, 27 and 28) with the algorithm of your choice. The available algorithms are defined in the ```stable_baselines3``` package.