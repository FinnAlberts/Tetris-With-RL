# Calculate the reward given gamestate and action
def get_reward(self, gamestate, action):
    # Initialize reward
    reward = 0

    # Check if game is over (penanlty of 250)
    if gamestate['is_game_over']:
        reward -= 250

    # Check if score has increased (reward of 100)
    # THIS DOES NOT WORK: gamestate['score'] is the same as self.score
    reward += (gamestate['score'] - self.score) * 100

    # Get a reward for distance fallen of the current tetronimo (reward of 1 per block)
    reward += (gamestate['average_height_of_current_tetronimo'])

    # Check if tetronimo has moved left or right (penalty of 0.1 to prevent useless movement)
    if action == 1 or action == 2:
        reward -= 0.1

    # Return the reward
    return reward