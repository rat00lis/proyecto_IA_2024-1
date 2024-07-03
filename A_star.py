from matrix import matrix_2048

import heapq
import copy

def snake_heuristic(state):
    snake_weight = [[ 10,   8,    7,    6.5],
                    [ 0.5,  0.7,  1,    3],
                    [-0.5, -1.5, -1.8, -2],
                    [-3.8, -3.7, -3.5, -3]]
    heuristic_value = 0
    for i in range(4):
        for j in range(4):
            heuristic_value += state[i][j] * snake_weight[i][j]
    return heuristic_value

class AStar2048:
    def __init__(self, initial_state):
        self.initial_state = initial_state
    
    def heuristic(self, state):
        return snake_heuristic(state)

    def a_star_search(self, state):
        moves = ['up', 'down', 'left', 'right']
        heuristic_values = []
        for move in moves:
            new_state = state.try_step(move)
            old_state = state.get_matrix()
            if new_state != old_state:
                heuristic_values.append(self.heuristic(new_state))
            else:
                heuristic_values.append(-100000000000)
        
        # rescatar en indice de mayor valor de heuristic_values
        # retornar indice de max value de heuristic_values
        best_move = -100000000000
        best_index = -1

        for i in range(len(heuristic_values)):
            if heuristic_values[i] > best_move:
                best_move = heuristic_values[i]
                best_index = i
        return best_index
    
    def init_algorithm(self,game):
        while game.game_over()!=False:
            direction = ['up', 'down', 'left', 'right']
            move = self.a_star_search(game)
            movement = getattr(game, direction[move], None)
            movement()
            game.add_number()
        return game.get_max_value()
        
# Inicialización de A*
max_value = 0
while max_value < 2048:
    game = matrix_2048()
    astar_solver = AStar2048(game)
    max_value = astar_solver.init_algorithm(game)
    print(f"Max value: {max_value}")
    game.print_matrix()
    print()

