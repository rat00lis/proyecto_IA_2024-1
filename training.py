from agent import *
from matrix import *


class trainer:
    def __init__(self, population_size, genome_size, mutation_rate, tree_height, num_episodes):
        self.game = matrix_2048()
        self.agent = agent(population_size, genome_size, mutation_rate, tree_height)
        self.last_score = 1
        self.num_episodes = num_episodes
        self.max_score = {
            "score": 0,
            "max_cell": 0,
        }
        self.score_list = []
        self.max_cell_list = []
    
    def send_move(self, move):
        if move == 0:
            self.game.down()
        elif move == 1:
            self.game.up()
        elif move == 2:
            self.game.left()
        elif move == 3:
            self.game.right()
        self.game.add_number()
    
    def get_data(self):
        score = self.game.get_score()
        board = self.game.get_matrix()
        return (score, board)
    
    def train(self):
        for i in range(self.num_episodes):
            self.agent.restart_game()
            self.game.restart()
            self.game.add_number()
            self.game.add_number()
            while True:
                score, board = self.get_data()
                move = self.agent.get_move(score, board)
                self.send_move(move)
                if self.game.game_over()!=None:
                    break
            if self.last_score < score:
                self.last_score = score
                self.max_score = score
            self.score_list.append(score)
            self.max_cell_list.append(self.game.get_max_value())




import csv
import os

def run_exp(population_sizes, genome_sizes, mutation_rates, tree_heights, num_episodes):
    os.makedirs('experimentos', exist_ok=True)
    final_scores = []  # Lista para almacenar el max_score de cada experimento

    for p in population_sizes:
        for g in genome_sizes:
            for m in mutation_rates:
                for t in tree_heights:
                    print(f"Population size: {p}, Genome size: {g}, Mutation rate: {m}, Tree height: {t}")
                    trainer_instance = trainer(p, g, m, t, num_episodes)
                    trainer_instance.train()
                    # Guardar los scores en un archivo CSV
                    score_filename = f"experimentos/scores_p{p}_g{g}_m{m}_t{t}_ep{num_episodes}.csv"
                    with open(score_filename, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Episode', 'Score'])
                        for episode, score in enumerate(trainer_instance.score_list):
                            writer.writerow([episode, score])
                    # Guardar los max cell en otro archivo CSV
                    max_cell_filename = f"experimentos/max_cells_p{p}_g{g}_m{m}_t{t}_ep{num_episodes}.csv"
                    with open(max_cell_filename, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Episode', 'Max Cell'])
                        for episode, max_cell in enumerate(trainer_instance.max_cell_list):
                            writer.writerow([episode, max_cell])
                    # Añadir el max_score al final_scores
                    final_scores.append(trainer_instance.max_score)
                    print(f"Results saved to {score_filename} and {max_cell_filename}\n")

    # Guardar el max_score de cada experimento en un archivo final
    final_scores_filename = "experimentos/final_max_scores.csv"
    with open(final_scores_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Experiment', 'Max Score', 'Max Cell'])
        for i, score in enumerate(final_scores):
            writer.writerow([i+1, score['score'], score['max_cell']])

population_sizes = [10, 100]
genome_sizes = [10, 100]
mutation_rates = [0.1]
tree_heights = [3, 7]
num_episodes = 10000

# run_exp(population_sizes, genome_sizes, mutation_rates, tree_heights, num_episodes)
import os
import csv
import matplotlib.pyplot as plt

def get_max_from_files():
    experiment_path = 'experimentos'
    score_files = [f for f in os.listdir(experiment_path) if f.startswith('scores')]
    max_scores = {}

    for file in score_files:
        with open(os.path.join(experiment_path, file), mode='r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            scores = [int(row[1]) for row in reader]
            max_score = max(scores)
            # Assuming file naming: scores_p{population}_g{genome}_m{mutation}_t{tree}_ep{episodes}.csv
            params = file.replace('scores_', '').replace('.csv', '')
            max_scores[params] = scores

    # Plotting and saving the last 5 max scores for each combination
    for params, scores in max_scores.items():
        plt.figure()
        plt.title(f"Last 5 Max Scores for {params}")
        plt.xlabel("Episode")
        plt.ylabel("Score")
        if len(scores) > 5:
            plt.plot(range(len(scores)-5, len(scores)), scores[-5:], marker='o')
        else:
            plt.plot(range(len(scores)), scores, marker='o')
        
        # Save the figure
        plt.savefig(f"{experiment_path}/max_scores_{params}.png")
        plt.close()  # Close the figure to free memory

get_max_from_files()