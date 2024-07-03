from matrix import matrix_2048

import heapq
import copy

def snake_heuristic(matrix):
    snake_weight = [[15, 14, 13, 12],
                    [8, 9, 10, 11],
                    [7, 6, 5, 4],
                    [0, 1, 2, 3]]
    heuristic_value = 0
    for i in range(4):
        for j in range(4):
            heuristic_value += matrix[i][j] * snake_weight[i][j]
    return heuristic_value


class AStar2048:
    def __init__(self, initial_matrix):
        self.initial_matrix = initial_matrix
    
    def heuristic(self, matrix):
        return snake_heuristic(matrix)

    def a_star_search(self, matrix):
        steps_matrixes = []
        moves = ['up', 'down', 'left', 'right']
        for move in moves:
            new_matrix = matrix.try_step(move)
            old_matrix = matrix.get_matrix()
            if new_matrix != old_matrix:
                steps_matrixes.append(new_matrix)
            else:
                steps_matrixes.append([[-100] * 4 for _ in range(4)])
        
        best_move = -1
        best_index = 0

        for i in range(len(steps_matrixes)):
            value = self.heuristic(steps_matrixes[i])
            if value > best_move:
                best_move = value
                best_index = i
        return best_index
    
    def init_algorithm(self,matrix):
        while matrix.game_over()!=False:
            direction = ['up', 'down', 'left', 'right']
            move = self.a_star_search(matrix)
            movement = getattr(matrix, direction[move], None)
            movement()
            matrix.add_number()
        return matrix.get_max_value()
        

# Inicialización de A*
max_value = 0
while max_value < 2048:
    initial_game = matrix_2048()
    astar_solver = AStar2048(initial_game)
    max_value = astar_solver.init_algorithm(initial_game)
    print(f"Max value: {max_value}")
    initial_game.print_matrix()
    print()

