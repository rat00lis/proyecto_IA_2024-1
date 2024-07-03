import copy
import random
from matrix import matrix_2048

class AStar2048:
    def __init__(self, initial_state):
        self.initial_state = initial_state
    
    def heuristic(self, state):
        # Define the snake weight pattern for heuristic evaluation
        snake_weight = [[10,    8,    7,    6.5],
                        [0.5,   0.7,  1,    3],
                        [-0.5, -1.5, -1.8, -2],
                        [-3.8, -3.7,  -3.5, -3]]
        
        heuristic_value = 0
        for i in range(4):
            for j in range(4):
                heuristic_value += state[i][j] * snake_weight[i][j]
        return heuristic_value

    def a_star_search(self, state):
        moves = ['up', 'down', 'left', 'right']
        heuristic_values = []
        for move in moves:
            new_state = state.try_step(move)
            old_state = state.get_state()
            if new_state != old_state:
                heuristic_values.append(self.heuristic(new_state))
            else:
                heuristic_values.append(float('-inf'))  # Use a more appropriate value for invalid moves
        
        best_value = max(heuristic_values)
        best_index = heuristic_values.index(best_value)
        return best_index if best_value != float('-inf') else -1
    
    def init_algorithm(self, game):
        while game.game_over() is None:

            # game.print_matrix()
            # print()

            directions = ['up', 'down', 'left', 'right']
            best_move = None
            best_value = float('-inf')

            # Descomentar si se quiere agregar heuristica para moverse automaticamente
            # hacia la "mejor" direccion
            # if random.random() < 0.5:
            #     # Use A* search to find the best move based on heuristic
            #     best_actual_move = directions[self.a_star_search(game)]
            #     if getattr(game, best_actual_move)():
            #         game.add_number()
            #     continue

            for move in directions:
                game_copy = copy.deepcopy(game)
                if getattr(game_copy, move)():
                    move_sum_value = 0
                    rollouts = 50
                    for _ in range(rollouts):
                        rollout_game = copy.deepcopy(game_copy)
                        while rollout_game.game_over() is None:
                            move_index = random.randint(0, 3)
                            getattr(rollout_game, directions[move_index])()
                            rollout_game.add_number()
                        move_sum_value += rollout_game.get_score()
                        # Prueba de valor como heuristica
                        # move_sum_value += self.heuristic(rollout_game.get_state())
                    
                    if move_sum_value > best_value:
                        best_value = move_sum_value
                        best_move = move
            
            if best_move:
                if getattr(game, best_move)():
                    game.add_number()
            else:
                break
        return game.get_max_value()

# Run the A* algorithm until the game is solved or it reaches a high value
max_value = 0
while max_value < 2048:
    game = matrix_2048()
    astar_solver = AStar2048(game)
    max_value = astar_solver.init_algorithm(game)
    print(f"Max value: {max_value}")
    game.print_matrix()
    print()
