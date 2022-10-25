# Calculate the reward given gamestate and action
def get_reward(self, gamestate, action):
    # Initialize reward
    reward = 0

    # Check if game is over (penanlty of 1000)
    if is_game_over(self.field):
        reward -= 1000

    # Check if score has increased (reward of 1000)
    reward += (self.score - self.previous_score) * 1000

    # Get a reward for choosing the best row (0.1 per empty block in row)
    x = self.tetronimo.blocks[0].get_x_in_blocks()
    for y in range(20):
        if self.field[y][x] == 0:
                reward += 0.1   

    # Check if tetronimo has moved left or right (penalty of 0.1 to prevent useless movement)
    if action == 1 or action == 2:
        reward -= 0.1

    # Return the reward
    return reward