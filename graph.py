import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

# Put the two graphs in 1 window
figure, (reward_graph, score_graph) = pyplot.subplots(2)

def graph():
    # Function for continuously updating the graphs
    def animate(i):
        # Read data from file
        pull_data = open("rewards.txt", "r").read()
        data = pull_data.split('\n')

        # Initialize x (run number), y (reward) and z (achieved in-game score) lists
        run_numbers = []
        rewards = []
        scores = []

        # Line index starts at 0
        index = 0

        # For each line of data
        for line in data:
            # If the line contains data
            if len(line) > 1:
                # Add the run number, reward and score to their respective lists
                reward, score = line.split(' ')
                run_numbers.append(int(index))
                rewards.append(float(reward))
                scores.append(float(score))
            # Update the line index number
            index += 1

        # Create a graph based on the reward for y and run number for x
        reward_graph.clear()
        reward_graph.plot(run_numbers, rewards)
        reward_graph.set_title("Reward Progression")
        reward_graph.set_xlabel("Run")
        reward_graph.set_ylabel("Reward")

        # Create a graph based on the score for y and run number for x
        score_graph.plot(run_numbers, scores)
        score_graph.set_title("Score progression")
        score_graph.set_xlabel("Run")
        score_graph.set_ylabel("Score")

    # Update the graphs every second
    animated = animation.FuncAnimation(figure, animate, interval=1000)

    # Show the graphs
    pyplot.show()


if __name__ == "__main__":
    graph()