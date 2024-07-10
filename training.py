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
    
    def train(self, start=0):
        for i in range(start, self.num_episodes):
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
        #guardar agente entrenado
        self.agent.save_agent()

import sys

#entrenar con argumentos por consola
if __name__ == '__main__':
    if len(sys.argv) == 6:
        population_size = int(sys.argv[1])
        genome_size = int(sys.argv[2])
        mutation_rate = float(sys.argv[3])
        tree_height = int(sys.argv[4])
        num_episodes = int(sys.argv[5])
        trainer = trainer(population_size, genome_size, mutation_rate, tree_height, num_episodes)
        trainer.train()
    else:
        print("Error: Wrong number of arguments")
        print("Usage: python3 training.py <population_size> <genome_size> <mutation_rate> <tree_height> <num_episodes>")
        print("Example: python3 training.py 100 100 0.1 5 100")